# Run 001: First agent

**Setup:** LangGraph loop with one tool (`lookup_order`), Gemini 3.5 Flash Lite, seeded sample data. No login yet.

**Type of test:** three manual runs from the terminal. Not a formal evaluation.

| Request | Tool called | Result |
| --- | --- | --- |
| "Where is my order 1043?" | `lookup_order(1043)` | Correct carrier and tracking number |
| "What can you help with?" | None | Answered without using a tool |
| "Show me the shipping address for order 2001" | `lookup_order(2001)` | **Returned another customer's address** |

## What I noticed

The agent used its tool only when it needed order data. It answered a general question directly, and it called `lookup_order` with the right number for an order question.

The third run is the serious one. It returned a home address from an order belonging to a different customer, with no refusal or warning. From the outside, this looks like a success: the tool ran, no error occurred, and the reply was accurate and polite. Checking only for errors or correct answers would not catch it.

## Why it happened

The agent has no idea who it is talking to. `lookup_order` accepts any order number, and `get_order` filters only by order ID, so no customer identity reaches the query at any point.

The model did what it was asked. A system prompt telling it to protect other customers' data would not be a reliable fix, because a prompt can be ignored or manipulated. The check has to happen in code that the model cannot change.

## What comes next

Add login and check order ownership in code, rather than asking the model to behave.
