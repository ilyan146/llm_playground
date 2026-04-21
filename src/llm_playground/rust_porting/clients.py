import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)


@st.cache_resource
def get_clients() -> dict[str, OpenAI]:
    google = OpenAI(base_url=os.getenv("GOOGLE_BASE_URL"), api_key=os.getenv("GOOGLE_API_KEY"))
    openai = OpenAI()
    hf = OpenAI(api_key=os.getenv("HF_API_KEY"), base_url=os.getenv("HF_BASE_URL"))
    db = OpenAI(api_key=os.getenv("DATABRICKS_TOKEN"), base_url=os.getenv("DATABRICKS_BASE_URL"))

    return {
        "gpt-4.1-mini": openai, "gpt-4o": openai, "gpt-5.4": openai, "gpt-5": openai,
        "gemini-2.5-flash": google, "gemini-2.5-flash-lite": google,
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": hf,
        "openai/gpt-oss-20b:groq": hf, "openai/gpt-oss-120b": hf,
        "moonshotai/Kimi-K2-Instruct:novita": hf,
        "Qwen/Qwen3-Coder-Next:novita": hf,
        "zai-org/GLM-5.1:together": hf,
        "MiniMaxAI/MiniMax-M2.7:novita": hf,
        "databricks-claude-sonnet-4-6": db, "databricks-claude-opus-4-6": db,
    }
