"""
LLM initialization and configuration.
Supports OpenAI and Groq — switch using LLM_PROVIDER in your .env file.

To use Groq (free):
    LLM_PROVIDER=groq

To use OpenAI (GPT-4o):
    LLM_PROVIDER=openai
"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

if LLM_PROVIDER == "groq":
    from langchain_groq import ChatGroq
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
    llm = ChatGroq(model="llama-3.1-8b-instant")
    print("[LLM] Using Groq — llama3-8b-8192 (free)")

else:
    from langchain_openai import ChatOpenAI
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    llm = ChatOpenAI(model="gpt-4o")
    print("[LLM] Using OpenAI — gpt-4o")
