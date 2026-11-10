# Architecture

Current state, before login. This page is updated as the system changes.

```mermaid
flowchart TD
    evals["Evals and terminal<br/>set the customer directly"]
    chat["POST /chat<br/>not logged in yet"]
    orders["GET /orders/{id}<br/>no ownership check yet"]

    subgraph loop["LangGraph loop"]
        agent["agent node<br/>replies or requests a tool"]
        tools["tools node<br/>runs lookup_order"]
        agent -- requests a tool --> tools
        tools -- tool result --> agent
    end

    gemini["Gemini 3.5 Flash Lite<br/>chooses tool, writes reply"]
    service["Order service<br/>only this customer's orders"]
    db[("Postgres<br/>customers, products, orders")]
    langsmith["LangSmith<br/>traces and experiments"]

    evals --> agent
    chat --> agent
    agent <--> gemini
    tools --> service
    service --> db
    orders --> db
    loop -.-> langsmith

    classDef enforced fill:#E1F5EE,stroke:#0F6E56,color:#085041
    classDef gap fill:#FAECE7,stroke:#993C1D,color:#712B13
    class service enforced
    class chat,orders gap
```

Teal marks a rule enforced in code. Coral marks a known gap that login will close.

## How a request flows

1. A request reaches the graph with a customer ID in its run configuration. The ID does not go through the model.
2. The agent node calls Gemini with the system prompt, the conversation and the tool definition. Gemini either replies or requests `lookup_order` with an order number.
3. The tools node runs `lookup_order`, which reads the customer ID from `ToolRuntime`. The model cannot see or change it.
4. The order service queries Postgres for that order only if it belongs to that customer.
5. The result goes back to the agent node, and Gemini writes the reply.

Each run is limited by a recursion limit, and each run can be traced in LangSmith.
