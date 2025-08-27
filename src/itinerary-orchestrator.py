import os
from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    # Load Gemini API key from environment variable
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    # Create a chat model instance
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.7
    )

    # Run a simple chat call
    response = chat_model.invoke("Write a haiku about the ocean")
    print(response.content)


if __name__ == "__main__":
    main()