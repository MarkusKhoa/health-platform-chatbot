# from langchain_community.llms import Ollama
# llm = Ollama(model="gemma2")
# res = llm.invoke("Why is the sky blue?")
# print(res)
import keyboard
from app.routers.v1.HealthAgentRouter import chat_search_agent
from loguru import logger

logger.add("Med_QA.log", 
           rotation="10 MB",  # Rotate log file after reaching 10 MB
           retention="10 days",  # Retain logs for 10 days
           compression="zip",  # Compress old logs
           format="{time} {level} {message}",  # Customize the format
           level="INFO"  # Log all INFO level messages and higher
          )

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('ESC'):
            print('Exiting program...')
            break
        message = input("Please enter question:")
        logger.info(f"User question: {message}")
        response = chat_search_agent(message=message)
        logger.info(f"Chatbot response: {response}")