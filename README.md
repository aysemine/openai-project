#  OpenAI Projects Playground

This repo is my little playground while learning how to use OpenAI – from basic function calling to LangChain, RAG, and even a tiny MCP-style agent.  
Each file is a mini step in figuring things out. Nothing fancy just trial & error.  

---

##  What's Inside?

- [main_basic_langchain.py](./main_basic_langchain.py): First steps with LangChain 
- [main_basic_raw_openai.py](./main_basic_raw_openai.py): A basic example of using OpenAI’s API without any helper libraries.  
- [main_openai_basic_structure.py](./main_openai_basic_structure.py): Trying to structure a simple OpenAI-based chatbot with clean input/output flow.  
- [main_openai_function_calling.py](./main_openai_function_calling.py): Practicing how to use OpenAI's function calling – feeding and parsing structured outputs.  
- [main_retrieval.py](./main_retrieval.py): A simple Retrieval-Augmented Generation (RAG) example using a JSON FAQ dataset [kb.json](./kb.json) to answer user questions by retrieving relevant information and generating responses with OpenAI.  
- [prompt_chaining.py](./prompt_chaining.py): Breaking tasks into steps and chaining prompts and routing mechanism (calendar assistant-style).  
- [main_mcp_experiment.py](./main_mcp_experiment.py): First experiment with an MCP-style architecture.

---

##  How to Run

This repo is mostly for learning and playing around with OpenAI tools, but if you're curious and want to try something out, here’s how:

### 1. Install dependencies

This project uses [`uv`](https://github.com/astral-sh/uv) and a [`pyproject.toml`](./pyproject.toml) file for dependency management.

To install dependencies:

```bash
uv pip install -r pyproject.toml
```
### 2. Set up your .env file
Make sure you have your OpenAI API key ready and stored in a `.env` file like this:

```bash
OPENAI_API_KEY=your-api-key-here
```
### 3. Run the scripts
Pick a script you want to explore and run it!

```bash
uv run main_openai_function_calling.py
```
Or just:

```bash
python main_openai_function_calling.py