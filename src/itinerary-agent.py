import os
from dotenv import load_dotenv
from flight_tool import search_flight
from hotel_tool import search_hotel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables!")

tools = [search_flight, search_hotel]  # Define your tools here if needed

# -------------------
#  Setup LLM + Agent
# -------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0
)

system_message = """
You are a Travel Itinerary Agent. 

- Your goal is to help users plan complete trips. 
- Use the available tools (flights, hotels, etc.) to fetch options.
- If the user input is incomplete, ask clear follow-up questions until you have all necessary details.
- Once you have enough information, summarize everything into a beautiful, structured travel itinerary in Markdown. 
- The final itinerary must include sections for Flights, Hotels, and Travel Notes, with icons and formatting.
"""


# -------------------
#  Create React Agent
# -------------------
checkpointer = MemorySaver()

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer
)


# -------------------
#  Main Loop
# -------------------
def main():
    thread = {"configurable": {"thread_id": "demo-thread"}}

    print("Welcome to the Travel Itinerary Agent!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter your message: ").strip()
        system_injected = False
        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        if not system_injected:
            # First call: include system message
            messages = [
                ("system", system_message),
                ("user", user_input)
            ]
            system_injected = True
        else:
            # Later calls: only user message
            messages = [("user", user_input)]

        response = agent.invoke({"messages": messages}, config=thread)

        print("\n Agent:\n", response["messages"][-1].content, "\n")


if __name__ == "__main__":
    main()