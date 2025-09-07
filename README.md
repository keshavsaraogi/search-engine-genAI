# Search Engine GenAI

A Streamlit chat application powered by LangChain and a Groq LLM that can search the web and cite information using three tools:

- DuckDuckGo web search
- Wikipedia
- arXiv

It maintains conversational memory, streams intermediate agent thoughts to the UI, and includes a companion notebook (`tools.ipynb`) that demonstrates building the same toolset and a simple RAG flow.

## Features

- Conversational agent with memory (`ConversationBufferMemory`).
- External tools: DuckDuckGo, Wikipedia, arXiv.
- Groq LLM with configurable model via `GROQ_MODEL`.
- Streamed callbacks to the UI for transparent tool usage.
- Notebook with RAG example using FAISS + OpenAI embeddings.

## Quick Start

Prerequisites:

- Python 3.10 or 3.11
- A Groq API key

Clone and run:

- Optional: create and activate a virtual env
  - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
  - Windows (PowerShell): `py -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Configure secrets (choose one)
  - Env var: `export GROQ_API_KEY="your_groq_key"`
  - `.env` file: add `GROQ_API_KEY="your_groq_key"` (the app auto-loads `.env`)
- Optional model selection: `export GROQ_MODEL="Llama3-70b-8192"`
- Run the app: `streamlit run app.py`
- Open: http://localhost:8501

## Using The Existing Conda Env (optional)

This repo currently contains a captured Conda environment directory at `search_engine_evn/`.

- Activate it: `conda activate ./search_engine_evn`
- Install/refresh deps inside it: `python -m pip install -r requirements.txt`
- Run: `python -m streamlit run app.py`

Note: This embedded environment is large and not portable; creating a fresh env is recommended for collaborators and CI.

## Dev Container / Codespaces

A devcontainer is provided in `.devcontainer/devcontainer.json`.

- Open the repo in a Dev Container or GitHub Codespace.
- Ports are forwarded automatically (8501).
- On first attach, requirements install and the Streamlit server starts automatically.

## Configuration

- `GROQ_API_KEY`: required. Set via environment or `.env`. The app first reads environment variables and only then tries `st.secrets` (safely guarded).
- `GROQ_MODEL`: optional. Defaults to `Llama3-70b-8192`. Override via environment or `.env`.

Supported Groq models change over time. If your chosen model is decommissioned, set `GROQ_MODEL` to a supported one suggested by Groq.

## Notebooks

`tools.ipynb` demonstrates:

- Building tools for DuckDuckGo, Wikipedia and arXiv.
- Creating an agent with those tools and a Groq LLM.
- A lightweight RAG flow using FAISS and OpenAI embeddings.

Run tips:

- Restart the kernel after changing environment variables.
- Ensure `GROQ_API_KEY` (and optionally `GROQ_MODEL`) are set in the notebook kernel environment.

## Project Structure

- `app.py`: Streamlit chat app that wires Groq + LangChain tools.
- `tools.ipynb`: Notebook demos for tools and RAG.
- `requirements.txt`: Python dependencies for the app and notebook.
- `.devcontainer/`: Dev environment that auto-runs the app on port 8501.
- `.github/workflows/main.yaml`: Placeholder CI to sync to Hugging Face Spaces (needs edits to be usable).
- `.env`: Local development env vars. Do not commit real secrets in production.

## Troubleshooting

- Streamlit secrets error (FileNotFoundError):
  - Fixed in the app. It now reads the env first and only safely checks `st.secrets` if present.
- Model decommissioned error from Groq:
  - Set `GROQ_MODEL` to a supported model, e.g., `Llama3-70b-8192`.
- Tool call validation failed (e.g., `brave_search` not in tools):
  - The notebook uses DuckDuckGo as `Search`. Ensure your `tools` list contains `search_tool`, and print `[t.name for t in tools]` to verify. The app already uses DuckDuckGo.
- Wrong interpreter / missing packages:
  - Confirm `which python` and `which streamlit` point to your active env.
  - If in doubt, run: `python -m pip install -r requirements.txt` and `python -m streamlit run app.py`.
- Pip resolver warnings:
  - `requirements.txt` is unpinned and may conflict with already-installed site packages. Prefer a clean env.

## Security Notes

- Do not commit API keys. Use environment variables, `.env` excluded by `.gitignore`, or Streamlit secrets in deployment.
- If keys have been committed previously, rotate them and purge from history where possible.

## Next Steps

- Clean and pin `requirements.txt` for reproducibility.
- Remove the embedded `search_engine_evn/` folder from version control.
- Add a proper Hugging Face Spaces workflow or alternative deploy (Streamlit Cloud, Fly.io, etc.).
- Add a sidebar model selector and tool toggles for quick experimentation.

---

Questions or issues? Open an issue or ask for help in the chat.

