# reply gAI

Reply gAI is an AI-powered personal assistant for Twitter/X users that creates interactive chatbot personas. It automatically collects a user's Tweets, stores them in long-term memory, and uses Retrieval-Augmented Generation (RAG) to generate responses that match their unique writing style and viewpoints.

![reply_gai](https://github.com/user-attachments/assets/91e5bf27-04c0-4584-817f-16e43296cd34)

## 🚀 Quickstart

One option for accessing Twitter/X data is the [Arcade API](https://docs.arcade-ai.com/integrations/toolkits/x) toolkit.

Set API keys for the LLM of choice (Anthropic API) along with the Arcade API:
```
export ANTHROPIC_API_KEY=<your_anthropic_api_key>
export ARCADE_API_KEY=<your_arcade_api_key>
export ARCADE_USER_ID=<your_arcade_user_id>
```

Clone the repository and launch the assistant [with the LangGraph server](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#dev):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/langchain-ai/reply_gAI.git
cd reply_gAI
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev
```

You should see the following output and Studio will open in your browser:

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

In the `configuration` tab, add the Twitter/X handle of any user: 

![Screenshot 2024-12-11 at 1 30 51 PM](https://github.com/user-attachments/assets/10cc592b-9b1d-4132-87e1-db3e65257fc9)

Then, just interact with a chatbot persona for that user:

![Screenshot 2024-12-11 at 1 30 30 PM](https://github.com/user-attachments/assets/6bbfbd5a-40a2-46c5-b329-c66e1c1952d8)

## How it works

Reply gAI uses LangGraph to create a workflow that mimics a Twitter user's writing style. Here's how the system operates:

1. **Tweet Collection**
   - Uses the [Arcade API X Toolkit](https://docs.arcade-ai.com/integrations/toolkits/x) to fetch Tweets over the past 7 days from a specified Twitter user
   - Tweets are stored in the LangGraph Server's [memory store](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store)
   - The system automatically refreshes tweets if they're older than the configured age limit

2. **Conversation Flow**
   - The workflow is managed by a state graph with two main nodes:
     - `get_tweets`: Fetches and stores recent tweets
     - `chat`: Generates responses using Claude 3.5 Sonnet

3. **Response Generation**
   - This uses RAG to condition responses based upon the user's Tweets stored in memory 
   - Currently, it loads all tweets into memory, but semantic search from the LangGraph Server's memory store [is also supported](https://langchain-ai.github.io/langgraph/concepts/persistence/#semantic-search)
   - The LLM analyzes the collected tweets to understand the user's writing style
   - It generates contextually appropriate responses that match the personality and tone of the target Twitter user

4. **Architecture**
   - Built on LangGraph for workflow management
   - Uses Anthropic's Claude 3.5 Sonnet for response generation
   - Integrates with Arcade API for Twitter data access
   - Maintains conversation state and tweet storage for efficient operation

The system automatically determines whether to fetch new tweets or use existing ones based on their age, ensuring responses are generated using recent and relevant data.

## Long-term memory

In the quickstart, we use a [locally running LangGraph server](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/#create-a-env-file). 

This uses the `langraph dev` command, which [launches the server in development mode](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#dev). 

Tweets are saved to the [LangGraph store](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store), which uses Postgres for persistence and is saved in the `.langgraph_api/` folder in this directory. 

You can visualize Tweets saved per each user in the Store directly with LangGraph Studio.

![Screenshot 2024-12-11 at 1 31 09 PM](https://github.com/user-attachments/assets/41a06245-0659-4309-b7e5-e78a2f108c2b)

## Deployment 

If you want to want to launch the server in a mode suitable for production, you can consider [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/quick_start/#langgraph-cloud-quick-start):

* Add `LANGSMITH_API_KEY` to your `.env` file.
* Ensure [Docker](https://docs.docker.com/engine/install/) is running on your machine.
* [Run with `langgraph up`](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#up)

```bash
luvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph up
```

See [Module 6](https://github.com/langchain-ai/langchain-academy/tree/main/module-6) of LangChain Academy for a detailed walkthrough of deployment options with LangGraph.
