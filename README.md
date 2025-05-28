# AWS-Multi-LLM-Agent-System
This repository contains a serverless, scalable system for automated customer feedback analysis using AWS Lambda, SQS, DynamoDB, and LLM-based NLP tools.

## Features

- Modular multi-agent architecture
- Dynamic tool selection based on user instructions
- Guardrail agent for safe user interaction
- End-to-end automation and scalable processing
- Robust, production-ready patterns

## Architecture

          +------------------+
          |    User/API      |
          +--------+---------+
                   |
                   v
      +-----------------------------+
      |  Lambda: AgentInference     |   <-- Handles user interaction, validation, guardrails
      +-----------------------------+
                   |
        (API call or SQS enqueue)
                   v
      +-----------------------------+
      |   Amazon SQS Queue          |   <-- Decouples ingestion from processing
      +-----------------------------+
                   |
                   v
      +-----------------------------+
      |  Lambda: AgentProcessor     |   <-- Runs NLP analysis tools, selects tools dynamically
      +-----------------------------+
                   |
                   v
      +-----------------------------+
      |    Amazon DynamoDB          |   <-- Stores feedback and analysis results
      +-----------------------------+

- **AgentInference Lambda**: Handles initial user/API interaction, input validation, and enforces guardrails. It interprets incoming requests and ensures only safe, valid instructions are passed to the backend.
- **Amazon SQS**: Decouples ingestion from processing, providing reliability and scalability.
- **AgentProcessor Lambda**: Receives SQS messages, dynamically selects and runs NLP tools based on the presence or absence of instructions, and stores results.
- **Amazon DynamoDB**: Securely stores original feedback and all analysis results for future querying and analytics.

---

## Key Features

- **Dynamic Tool Selection**: Uses LLMs to determine which analysis tools to run based on user instructions, or defaults to running all tools if no instructions are provided.
- **Multi-Agent Structure**: Separates user interaction and processing logic, improving maintainability and compliance with best practices.
- **Robust Guardrails**: Ensures all user inputs are validated and safe before processing.
- **Idempotency**: Prevents duplicate processing of feedback using DynamoDB checks.
- **End-to-End Automation**: The entire workflow, from input to storage, is automated and scalable.
- **Extensible**: Easily add new NLP tools, agents, or integrations.
- **Production-Ready**: Includes error handling, logging, monitoring hooks, and follows AWS security best practices

## Getting Started

1. Deploy infrastructure using your preferred IaC tool (CloudFormation, SAM, Terraform).
2. Deploy Lambda functions.
3. Configure SQS, DynamoDB, and API keys/secrets.
4. Send feedback data to SQS and monitor results in DynamoDB.

## How It Works

1. **User submits feedback** via API or web interface.
2. **AgentInference Lambda** receives input, validates it, applies guardrails, and passes the request to SQS.
3. **AgentProcessor Lambda** is triggered by SQS, checks if the feedback has already been processed (idempotency), determines which NLP tools to run (dynamically via LLM or defaults), and performs the analysis.
4. **Results and original feedback** are securely stored in DynamoDB for future access and reporting.


## Example Feedback Payload

```json
{
  "feedback_id": "781",
  "customer_name": "Derek",
  "feedback_text": "Website was easy to navigate, but I had trouble applying a discount code.",
  "timestamp": "2025-05-28T12:00:00Z",
  "instructions": ""
}
```

- If `instructions` is empty or missing, all analysis tools run.
- If `instructions` are present, dynamic tool selection is used.

---

## Strengths in the Current System
1. Handles missing/empty instructions gracefully (always runs default tools).
2. No unnecessary LLM/Groq API calls when instructions are missing/empty.
3. Results are structured and stored in DynamoDB.
4. Logging is present for processing and error tracking.
5. Modular tool-running logic (sentiment, topic, etc.).
6. Short feedback (runs all tools, though some results may be trivial/empty).
7. Long feedback (runs all tools, gets richer, more meaningful LLM responses).
   
"Agent uses an LLM (Groq) to interpret instructions and select tools:
Even if instructions aren’t present, your fallback ensures all tools are run, which is acceptable per your requirements.
Default tool execution:
If no instructions are given or LLM selection fails, all tools execute.
Robust error handling:
If the LLM call fails or the response is malformed, the workflow continues without crashing."



## Acknowledgements

- AWS Lambda, SQS, DynamoDB
- OpenAI/Groq for LLM-powered tool selection
- All contributors and testers

