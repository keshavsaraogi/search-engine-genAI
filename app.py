import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory

import os
from dotenv import load_dotenv

load_dotenv()

# Secrets/config
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

if api_key is None:
    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

## Tools
wikiWrapperAPI = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxivAPIWrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)

wiki = WikipediaQueryRun(api_wrapper = wikiWrapperAPI)
arxiv = ArxivQueryRun(api_wrapper = arxivAPIWrapper)

search = DuckDuckGoSearchAPIWrapper()

search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events"
)

st.title("🔎 Langchain - Chat with Search")

default_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
available_models = list({
    default_model: None,
    "llama-3.1-8b-instant": None,
}.keys())

selected_model = st.sidebar.selectbox(
    "Groq model",
    options=available_models,
    index=0,
    help="Override the GROQ_MODEL env var at runtime",
)

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

    llm = ChatGroq(groq_api_key=api_key, model_name=selected_model, streaming=True)
    tools = [search_tool, wiki, arxiv]

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
