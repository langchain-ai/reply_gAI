import uuid
import os
from datetime import datetime, timezone
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain_anthropic import ChatAnthropic 
from langgraph.graph import MessagesState
from langgraph.store.base import BaseStore
from langgraph.graph import END, StateGraph
from arcadepy import Arcade

import agent.configuration as configuration
from agent.prompts import CHAT_INSTRUCTIONS
from agent.utils import get_all_tweets

def get_tweets(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Fetch and store recent tweets for a specified Twitter user.
    
    This function authenticates with the Arcade API, retrieves recent tweets for a given
    username, and stores them in the provided BaseStore instance. Each tweet is stored
    with its text content and URL.
    
    Args:
        state (MessagesState): Current conversation state (unused but required by graph)
        config (RunnableConfig): Configuration object containing settings like username
        store (BaseStore): Storage interface for saving retrieved tweets
        
    Returns:
        dict: Empty dictionary (function stores tweets but doesn't return them)
        
    Note:
        - Requires ARCADE_USER_ID environment variable to be set
        - Fetches up to 100 most recent tweets from the last 7 days
        - Stores tweets using (username, "tweets") as namespace
    """

    # Get the configuration
    configurable = configuration.Configuration.from_runnable_config(config)

    client = Arcade()  
    USER_ID = os.environ["ARCADE_USER_ID"]
    TOOL_NAME = "X.SearchRecentTweetsByUsername"

    auth_response = client.tools.authorize(
        tool_name=TOOL_NAME,
        user_id=USER_ID,
    )

    if auth_response.status != "completed":
        print(f"Click this link to authorize: {auth_response.authorization_url}")

    # Wait for the authorization to complete
    client.auth.wait_for_completion(auth_response)

    # Search for recent tweets (last 7 days) on X (Twitter)
    username = configurable.username

    # Get all the tweets
    tweets = get_all_tweets(client, username, USER_ID, TOOL_NAME)

    # Load the tweets into memory
    namespace_for_memory = (username, "tweets")
    for tweet in tweets:
        memory_id = tweet.get('id',uuid.uuid4())
        text = tweet.get('text',"Tweet empty")
        url = tweet.get('tweet_url',"URL not found")
        store.put(namespace_for_memory, memory_id, {"text": text,"url": url})

def chat(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Generate a chat response in the style of a specific Twitter user.
    
    This function retrieves tweets from the store for a given username, formats them,
    and uses them as context for Claude to generate a response that mimics the user's
    writing style and personality.

    Args:
        state (MessagesState): Current conversation state containing message history
        config (RunnableConfig): Configuration object containing settings like username
        store (BaseStore): Storage interface for accessing saved tweets

    Returns:
        dict: Contains the generated message in the 'messages' key
    """

    # Get the configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    username = configurable.username
    
    # Get the tweets
    namespace_for_memory = (username, "tweets")

    # Get all the tweets
    memories = []
    while mems := store.search(namespace_for_memory, limit=200, offset=len(memories)):
        memories.extend(mems)
        
    # Format the tweets
    formatted_output = ""
    for memory in memories:
        tweet = memory.value
        formatted_output += f"@{username}: {tweet['text']}\n"
        formatted_output += "-" * 80 + "\n"

    # Generate a response
    claude_3_5_sonnet = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.75) 
    chat_instructions_formatted = CHAT_INSTRUCTIONS.format(username=username,tweets=formatted_output)
    msg = claude_3_5_sonnet.invoke([SystemMessage(content=chat_instructions_formatted)]+state['messages'])
    return {"messages": [msg]} 

def route_to_tweet_loader(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Route the workflow based on tweet availability and age.
    
    This function determines whether to fetch new tweets or proceed to chat by checking:
    1. If tweets exist for the user in the store
    2. If existing tweets are too old (beyond max_tweet_age_seconds)
    
    Args:
        state (MessagesState): Current conversation state
        config (RunnableConfig): Configuration containing username and tweet age settings
        store (BaseStore): Storage interface for accessing saved tweets
        
    Returns:
        str: Either "get_tweets" to fetch new tweets or "chat" to proceed with conversation
    """

     # Get the configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    username = configurable.username
    
    # If we have Tweets from the user, go to chat
    namespace_for_memory = (username, "tweets")
    memories = store.search(namespace_for_memory, limit=200)

    # If we have tweets, check if they're too old
    if memories:    
        # Get most recent tweet timestamp
        most_recent = max(mem.created_at for mem in memories)
        
        # Calculate time difference
        now = datetime.now(timezone.utc)
        time_delta = now - most_recent
        
        # If tweets are too old, get new ones
        if time_delta.total_seconds() > configurable.max_tweet_age_seconds:
            return "get_tweets"
        return "chat"
    # If no tweets for the user, get them 
    else:
        return "get_tweets"

# Create the graph + all nodes
builder = StateGraph(MessagesState, config_schema=configuration.Configuration)
builder.add_node("chat",chat)
builder.add_node("get_tweets",get_tweets)
builder.set_conditional_entry_point(route_to_tweet_loader, ["chat", "get_tweets"])
builder.add_edge("get_tweets", "chat")
builder.add_edge("chat", END)

# Compile the graph
graph = builder.compile()