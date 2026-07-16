import logging
import os
import json

from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

try:
    from langchain_openai import ChatOpenAI
except ImportError:  # pragma: no cover - optional dependency path
    ChatOpenAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # pragma: no cover - optional dependency path
    ChatGoogleGenerativeAI = None


class Agent:
    def __init__(self, provider=None, model_name=None):
        logging.debug("INITIALIZATION STARTED")

        provider = (provider or os.getenv("AI_PROVIDER", "openai")).lower()
        tools = [self.fetch_verse]
        system_message = SystemMessage(
            content="""You are an Expert at Quranic Texts and Books of Hadith. Based on User's input, understand their emotions and provide a Chapter No. and Verse Number that is related and find the translation from the agent. "verse_key" example "3:14" indicating chapter 3 verse 14. Respond like an Imam. End the statement by recognizing that only Allah knows the best."""
        )

        if provider == "gemini":
            if ChatGoogleGenerativeAI is None:
                raise ImportError("Install langchain-google-genai to use the Gemini provider.")

            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY before using the gemini provider.")

            model = ChatGoogleGenerativeAI(
                model=model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
                google_api_key=api_key,
            )
        else:
            if ChatOpenAI is None:
                raise ImportError("Install langchain-openai to use the OpenAI provider.")

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("Set OPENAI_API_KEY before using the openai provider.")

            model = ChatOpenAI(model=model_name or os.getenv("OPENAI_MODEL", "gpt-4o"))

        self.provider = provider
        self.app = create_react_agent(model, tools, prompt=system_message, debug=True)

    def invoke(self, query, chat_history):
        """Returns app to invoke and create chain."""
        return self.app.invoke(
            {
                "messages": chat_history + [("human", query)]
            },
        )["messages"][-1].content.strip()

    @tool
    def fetch_verse(verse_key: str) -> str:
        """Provides verse translation based on user verse_key example: 6:16."""
        logging.debug("Assisting")

        if os.path.exists("./docs/all_verses.json"):
            with open("./docs/all_verses.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                for verse in data:
                    if verse["verse_key"] == verse_key:
                        return verse["translation"]

        return "No response"
