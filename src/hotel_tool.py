import os
from typing import Optional
from langchain.tools import tool
from dotenv import load_dotenv
import serpapi


load_dotenv()

SERP_API_KEY = os.environ.get("SERP_API_KEY")


@tool
def search_hotel(
    query: Optional[str] = None,
    check_in_date: Optional[str] = None,
    check_out_date: Optional[str] = None,
    currency: Optional[str] = "USD"
) -> str:
    """
    A tool to search for hotels using SerpAPI and get top 3 hotels and their details sorted by highest rating.

    Args:
        query: The query to search for. Example: "Near the Eiffel Tower in Paris".
        check_in_date: The check-in date in 'YYYY-MM-DD' format.
        check_out_date: The check-out date in 'YYYY-MM-DD' format.
        currency: The currency to use for the search.

    Returns:
        The search results.
    """
    if query is None:
        raise ValueError("Query cannot be None")

    client = serpapi.Client(api_key=SERP_API_KEY)
    results = client.search(
        engine="google_hotels",
        hl="en",
        gl="us",
        q=query,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        currency=currency,
        sort_by= "8"
    )

    # Get the local results
    local_results = results['properties']

    # Sort the local results by rating in descending order
    sorted_results = sorted(local_results, key=lambda x: x['overall_rating'], reverse=True)

    # Get the top 3 hotels
    top_3_hotels = sorted_results[:3]

    return str(top_3_hotels)


if __name__ == "__main__":

    print("Searching hotels...\n")
    
    result = search_hotel.invoke({
        "query": "Paris",
        "check_in_date": "2025-08-27",
        "check_out_date": "2025-08-28",
        "currency": "USD"
    })

    print(result)