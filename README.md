# Reply gAI

Reply gAI is an AI-powered personal assistant for Twitter/X users that creates interactive chatbot personas. It automatically collects a user's Tweets, stores them in long-term memory, and uses Retrieval-Augmented Generation (RAG) to generate responses that match their unique writing style and viewpoints.

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

![Screenshot 2024-12-06 at 4 15 39 PM](https://github.com/user-attachments/assets/c9a12f72-4f45-42a9-b8a6-e30cc15128c4)

You can interact with a chatbot persona for that user:

![Screenshot 2024-12-06 at 4 15 14 PM](https://github.com/user-attachments/assets/bd39a211-34c3-4d72-87ef-79efb382e334)

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

Tweets are saved to the LangGraph store, which uses Postgres as is saved in the `.langgraph_api/` directory. 

## Deployment 

If you want to want to launch the server in a mode suitable for production, you can consider [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/quick_start/#langgraph-cloud-quick-start):

* Add `LANGSMITH_API_KEY` to your `.env` file.
* Ensure [Docker](https://docs.docker.com/engine/install/) is running on your machine.
* [Run with `langgraph up`](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#up): `luvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph up`

See [Module 6](https://github.com/langchain-ai/langchain-academy/tree/main/module-6) of LangChain Academy for a detailed walkthrough of deployment options with LangGraph.