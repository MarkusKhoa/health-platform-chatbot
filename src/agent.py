import os
import json

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core import StorageContext
from config import STORAGE_PATH, CACHE_FILE_PATH, INDEX_STORAGE_PATH

from tools import query_engine, query_tool
from prompts import HEATH_AGENT_PROMPT

class HealthAgent:
    def __init__(self, chat_store, container, username, user_info):
        self.chat_store = chat_store
        self.container = container
        self.username = username
        self.user_info = user_info
    
    def chat(self, question):
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=800,
            chat_store=self.chat_store,
            chat_store_key=self.username
        )
        query_engine = query_engine
        query_tool = query_tool
        
        agent = OpenAIAgent.from_tools(tools=[query_engine, query_tool],
                                       memory=memory, system_prompt=HEATH_AGENT_PROMPT)
        response = agent.chat()
        