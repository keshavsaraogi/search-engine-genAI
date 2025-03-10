import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

import os
from dotenv import load_dotenv

## Tools
wikiWrapperAPI = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxivAPIWrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)

wiki = WikipediaQueryRun(api_wrapper=wikiWrapperAPI)
arxiv = ArxivQueryRun(api_wrapper=arxivAPIWrapper)

search = DuckDuckGoSearchAPIWrapper()

## Streamlit Application
st.title("Langchain - Chat with Search")

## Sidebar Settings
st.sidebar.title("Settings")
apiKey = st.sidebar.text_input("Enter your Groq API KEY: ", type="password")

