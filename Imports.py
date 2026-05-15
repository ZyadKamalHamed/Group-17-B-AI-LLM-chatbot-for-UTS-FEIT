import os
import sys
import subprocess
import time
import threading
import queue
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager
import asyncio
from concurrent.futures import ThreadPoolExecutor


def install_packages():
    """Install required packages for Colab environment"""
    packages = [
        "langchain",
        "langchain-community",
        "langchain-core",
        "chromadb",
        "sentence-transformers",
        "faiss-cpu",
        "pypdf",
        "python-docx",
        "requests",
        "psutil",
        "pyngrok",
        "gradio"
    ]
   
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])




import requests
import psutil
import threading
from queue import Queue
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationChain, RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS, Chroma
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.embeddings import OllamaEmbeddings
