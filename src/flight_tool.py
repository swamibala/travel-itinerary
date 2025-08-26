import os
from typing import Optional
from langchain.tools import tool
from dotenv import load_dotenv
import serpapi


load_dotenv()

SERP_API_KEY = os.environ.get("SERP_API_KEY")

def format_duration(minutes: int) -> str:
    """Convert duration in minutes into 'Xh Ym' format."""
    try:
        minutes = int(minutes)
        hours, mins = divmod(minutes, 60)
        return f"{hours}h {mins}m"
    except Exception:
        return str(minutes)

@tool
def search_flight(
    originLocationCode: str,
    destinationLocationCode: str,
    departureDate: str,
    returnDate: Optional[str] = None,
    adults: int = 1,
    travelClass: Optional[str] = None
) -> str:
    """
    Search for flights using SerpAPI's Google Flights and return the top 3 options.
    Looks first in 'best_flights', then falls back to 'other_flights'.
    """

    if not SERP_API_KEY:
        return "SERP_API_KEY not found in environment variables."

    try:
        client = serpapi.Client(api_key=SERP_API_KEY)
        results = client.search(
            engine="google_flights",
            hl="en",
            gl="us",
            departure_id=originLocationCode,
            arrival_id=destinationLocationCode,
            outbound_date=departureDate,
            return_date=returnDate,
            currency="USD",
            adults=adults
        )

        # Prefer best_flights, else fallback to other_flights
        flights = results.get("best_flights") or results.get("other_flights", [])
        if not flights:
            return "No flights found for the given criteria."

        top_flights = flights[:3]
        response_lines = []

        for idx, flight in enumerate(top_flights, 1):
            price = flight.get("price", "N/A")
            total_duration = format_duration(flight.get("total_duration", "N/A"))

            # Each flight option may include multiple legs
            flight_segments = []
            for seg in flight.get("flights", []):
                dep = seg.get("departure_airport", {})
                arr = seg.get("arrival_airport", {})
                airline = seg.get("airline", "Unknown Airline")
                fnum = seg.get("flight_number", "")
                dep_info = f"{dep.get('name', '')} ({dep.get('id', '')}) at {dep.get('time', '')}"
                arr_info = f"{arr.get('name', '')} ({arr.get('id', '')}) at {arr.get('time', '')}"
                seg_duration = format_duration(seg.get("duration", 0))
                flight_segments.append(
                    f"{airline} {fnum}: {dep_info} → {arr_info} ({seg_duration})"
                )

            # Add layovers if present
            layovers = flight.get("layovers", [])
            layover_info = ""
            if layovers:
                layover_info = " | Layovers: " + ", ".join(
                    f"{l.get('name')} ({l.get('id')}) {format_duration(l.get('duration', 0))}"
                    for l in layovers
                )

            response_lines.append(
                f"{idx}. Price: ${price}, Duration: {total_duration}\n"
                + "\n   ".join(flight_segments)
                + layover_info
            )

        return "\n\n".join(response_lines)

    except Exception as e:
        return f"Error searching flights: {str(e)}"


def main():
    # Set your SERP API key (or make sure it is set in environment)
    if not os.environ.get("SERP_API_KEY"):
        os.environ["SERP_API_KEY"] = "your_serp_api_key_here"

    # Sample request: Paris (CDG) → Tokyo (NRT)
    origin = "CDG"   # Paris Charles de Gaulle
    destination = "NRT"  # Tokyo Narita
    departure_date = "2025-09-01"
    return_date = "2025-09-10"
    adults = 1
    travel_class = "ECONOMY"

    print("🔍 Searching flights...\n")
    result = search_flight.invoke({
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "returnDate": return_date,
        "adults": adults,
        "travelClass": travel_class,
    })
    print(result)


if __name__ == "__main__":
    main()