import os
import sys
from typing import Any
from google import genai

MODEL_ID = "gemini-decision-1"

ORDER_QUESTIONS: dict[str, Any] = {
    "drink_type": {
        "type": "choice",
        "instructions": "Identify the base coffee drink type requested by the customer.",
        "criteria": {
            "Espresso": "Strong concentrated coffee served in small shots.",
            "Americano": "Espresso diluted with hot water.",
            "Latte": "Espresso with a large amount of steamed milk and light foam.",
            "Cappuccino": "Espresso with equal parts steamed milk and thick milk foam.",
            "Mocha": "Espresso mixed with chocolate syrup and steamed milk.",
        },
    },
    "milk_type": {
        "type": "choice",
        "instructions": "Identify the type of milk preferred by the customer. If not specified, default to Whole Milk.",
        "criteria": {
            "Whole Milk": "Standard dairy whole milk.",
            "Skim Milk": "Fat-free or skimmed dairy milk.",
            "Oat Milk": "Plant-based milk made from oats.",
            "Soy Milk": "Plant-based milk made from soybeans.",
            "Almond Milk": "Plant-based milk made from almonds.",
        },
    },
    "size": {
        "type": "choice",
        "instructions": "Identify the size of the drink. Default to Medium if not specified.",
        "criteria": {
            "Small": "Small size cup.",
            "Medium": "Medium or regular size cup.",
            "Large": "Large or tall/grande size cup.",
        },
    },
    "temperature": {
        "type": "choice",
        "instructions": "Identify if the customer wants the drink hot or cold/iced. Default to Hot if not specified.",
        "criteria": {
            "Hot": "Served hot.",
            "Iced": "Served cold with ice.",
        },
    },
    "syrup": {
        "type": "choice",
        "instructions": "Identify the flavor syrup requested. Default to None if not specified.",
        "criteria": {
            "None": "No flavor syrup or sugar syrup requested.",
            "Vanilla": "Vanilla flavored syrup.",
            "Caramel": "Caramel flavored syrup.",
            "Hazelnut": "Hazelnut flavored syrup.",
            "Chocolate": "Chocolate or mocha flavored syrup.",
            "Toffee Nut": "Toffee nut flavored syrup.",
        },
    },
    "extra_shots": {
        "type": "choice",
        "instructions": "Identify the number of extra espresso shots requested.",
        "criteria": {
            "0": "No extra shots requested.",
            "1": "One additional espresso shot.",
            "2": "Two additional espresso shots.",
            "3": "Three or more additional espresso shots.",
        },
    },
}


def get_client() -> genai.Client:
    """Initializes the GenAI client using the GEMINI_API_KEY environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY environment variable not found. "
            "Set it via `export GEMINI_API_KEY='your-key'`."
        )
    return genai.Client(api_key=api_key)


def parse_coffee_order(client: genai.Client, order_text: str) -> dict[str, dict[str, Any]]:
    """Converts a free-text coffee order into structured decisions."""
    result = client.decisions.create(
        model=MODEL_ID,
        input=order_text,
        questions=ORDER_QUESTIONS,
    )

    return {
        field: {
            "choice": answer.choice,
            "confidence": round(answer.confidence, 4),
        }
        for field, answer in result.answers.items()
    }


def print_receipt(order_text: str, parsed_order: dict[str, dict[str, Any]]) -> None:
    """Formats and prints the structured decision output."""
    print("=" * 55)
    print(f"INPUT ORDER : {order_text}")
    print("-" * 55)
    for field, data in parsed_order.items():
        label = field.replace("_", " ").title()
        print(f"{label:<13}: {data['choice']:<12} (confidence={data['confidence']:.2f})")
    print("=" * 55)


def main() -> None:
    # Accept order from command-line arguments or fall back to a default example
    order_input = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "I want a large iced oat milk latte with 2 extra shots and vanilla syrup"
    )

    client = get_client()
    parsed_order = parse_coffee_order(client, order_input)
    print_receipt(order_input, parsed_order)


if __name__ == "__main__":
    main()
