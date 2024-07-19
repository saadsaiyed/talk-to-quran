import logging, os, json
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

class Agent():
    def __init__(self):
        logging.debug(f"INITIALIZATION STARTED")
        
        model = ChatOpenAI(model="gpt-4o")
        tools = [self.fetch_verse]
        system_message = SystemMessage(content=f"""You are an Expert at Quranic Texts and Books of Hadith. Based on User's input, understand their emotions and provide a Chapter No. and Verse Number that is related and find the translation from the agent. "verse_key" example "3:14" indicating chapter 3 verse 14.""")
        self.app = create_react_agent(model, tools, messages_modifier=system_message, debug=True)
    
    def invoke(self, query):
        """Returns app to invoke and create chain"""
        return self.app.invoke(
            {
                "messages": [
                    ("human", query)
                ]
            },
        )["messages"][-1].content.strip()

    @tool
    def fetch_verse(verse_key: str) -> str:
        """Provides verse translation based on user verse_key example: 6:16"""
        logging.debug("Assisting")

        if os.path.exists("./docs/all_verses.json"):
            with open("./docs/all_verses.json", 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)        
                for verse in data:
                    if verse["verse_key"] == verse_key:
                        return verse["translation"]

        return "No response"

