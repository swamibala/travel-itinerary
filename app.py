import os
from dotenv import load_dotenv
from src.itinerary_agent import TravelItineraryAgent


# -------------------
#  Main Loop
# -------------------
def main():
    thread = {"configurable": {"thread_id": "demo-thread"}}

    agent = TravelItineraryAgent()


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
                ("system", agent.system_message),
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