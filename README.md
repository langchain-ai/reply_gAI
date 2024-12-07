# Reply gAI

## 🚀 Quickstart with LangGraph server

Sign up for an [Arcade API](https://docs.arcade-ai.com/integrations/toolkits/x) to get access to Twitter data.

Install the langgraph CLI:
```
pip install -U "langgraph-cli[inmem]"
```

Install dependencies:
```
pip install -e .
```

Load API keys into the environment for the LangSmith SDK, Anthropic API and Tavily API:
```
export ANTHROPIC_API_KEY=<your_anthropic_api_key>
export ARCADE_API_KEY=<your_arcade_api_key>
export ARCADE_USER_ID=<your_arcade_user_id>
```

Launch the agent:
```
langgraph dev
```

If all is well, you should see the following output:

> Ready!

> API: http://127.0.0.1:2024

> Docs: http://127.0.0.1:2024/docs

> LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## How it works

Reply gAI uses LangGraph to create a workflow that mimics a Twitter user's writing style. Here's how the system operates:

1. **Tweet Collection**
   - Uses the [Arcade API X Toolkit](https://docs.arcade-ai.com/integrations/toolkits/x) to fetch up to 100 recent tweets from a specified Twitter user
   - Tweets are stored locally with their text content and URLs
   - The system automatically refreshes tweets if they're older than the configured age limit

2. **Conversation Flow**
   - The workflow is managed by a state graph with two main nodes:
     - `get_tweets`: Fetches and stores recent tweets
     - `chat`: Generates responses using Claude 3.5 Sonnet

3. **Response Generation**
   - Claude analyzes the collected tweets to understand the user's writing style
   - Generates contextually appropriate responses that match the personality and tone of the target Twitter user
   - Uses a temperature of 0.75 to balance creativity with consistency

4. **Architecture**
   - Built on LangGraph for workflow management
   - Uses Anthropic's Claude 3.5 Sonnet for response generation
   - Integrates with Arcade API for Twitter data access
   - Maintains conversation state and tweet storage for efficient operation

The system automatically determines whether to fetch new tweets or use existing ones based on their age, ensuring responses are generated using recent and relevant data.
