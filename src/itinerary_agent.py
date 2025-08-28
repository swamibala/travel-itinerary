import os
from dotenv import load_dotenv
from .flight_tool import search_flight
from .hotel_tool import search_hotel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


load_dotenv()


class TravelItineraryAgent:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("Missing GOOGLE_API_KEY in environment variables!")

        self.tools = [search_flight, search_hotel]  # Define your tools here if needed

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.google_api_key,
            temperature=0
        )

        self.system_message = """
        You are a Travel Itinerary Agent. 

        - Your goal is to help users plan complete trips. 
        - Use the available tools (flights, hotels, etc.) to fetch options.
        - If the user input is incomplete, ask clear follow-up questions until you have all necessary details.
        - Once you have enough information, summarize everything into a beautiful, structured travel itinerary in Markdown. 
        - The final itinerary must include sections for Flights, Hotels, and Travel Notes, with icons and formatting.
        """

        self.checkpointer = MemorySaver()

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.checkpointer
        )
    

    def invoke(self, input, config=None):
        return self.agent.invoke(input, config=config)