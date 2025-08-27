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

        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        response = agent.invoke(
            {"messages": [("user", user_input)]},
            config=thread
        )

        print("\nAgent:", response["messages"][-1].content, "\n")


if __name__ == "__main__":
    main()