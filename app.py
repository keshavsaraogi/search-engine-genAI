import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Groq API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")

if api_key is None:
    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()  # Stop execution if the API key is missing

## Tools
wikiWrapperAPI = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxivAPIWrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)

wiki = WikipediaQueryRun(api_wrapper = wikiWrapperAPI)
arxiv = ArxivQueryRun(api_wrapper = arxivAPIWrapper)

search = DuckDuckGoSearchAPIWrapper()

# Create a custom tool for the search wrapper.
search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events"
)

## Streamlit Application
st.title("🔎 Langchain - Chat with Search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am a Chatbot who can search the web. How can I help you?"}
    ]

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input(placeholder="What is Machine Learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
    tools = [search_tool, wiki, arxiv]

    # Use AgentType.CONVERSATIONAL_REACT_DESCRIPTION
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=st.session_state.memory,
        handle_parsing_errors=True,
    )

    with st.chat_message("assistant"):
        streamlitCallback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        response = agent_chain.run(input=prompt, callbacks=[streamlitCallback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)