# coffee_order_parser
A lightweight Python CLI and module that converts unstructured, free-text customer coffee orders into structured selections with confidence scores using the **Gemini Decisions API** (`gemini-decision-1`).
# Coffee Order Parser (`gemini-decision-1`)

## Features

- **Structured Classification:** Maps natural language orders to predefined menu criteria (`drink_type`, `milk_type`, `size`, `temperature`, `syrup`, `extra_shots`).
- **Smart Defaults:** Automatically resolves unspecified attributes (e.g., defaults to `Medium`, `Hot`, `Whole Milk`, and `None` for syrup).
- **Confidence Scoring:** Returns model confidence values for every parsed attribute.
- **CLI & Module Ready:** Run directly from the terminal or import `parse_coffee_order()` into an existing POS or ordering pipeline.

---

## Prerequisites

- Python **3.10+**
- A valid **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/) with access to `gemini-decision-1`.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bukempas/coffee_order_parser.git](https://github.com/bukempas/coffee_order_parser.git)
   cd coffee-order-parser
