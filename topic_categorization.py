import json
from groq import Groq

def categorize(text: str) -> dict:
    """
    Categorizes the input feedback text into one or more predefined topics
    using the Groq LLM. Returns the primary topic, secondary topics (if any),
    and a confidence score between 0.0 and 1.0.

    Args:
        text (str): The feedback text to categorize.

    Returns:
        dict: {
            "primary_topic": str,
            "secondary_topics": List[str],
            "confidence": float
        }
        or an error message if categorization fails.
    """
    client = Groq()
    prompt = (
        "Categorize this text using these topics: "
        "[Product Quality, Delivery, Support, Pricing, Features, Other].\n"
        "Return ONLY valid JSON in this exact format:\n"
        '{\n'
        '  "primary_topic": "category",\n'
        '  "secondary_topics": ["category1", "category2"],\n'
        '  "confidence": 0.0-1.0\n'
        '}\n'
        f"Text: {text}"
    )
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.0  # Force deterministic output
        )
        llm_response = response.choices[0].message.content.strip()
        print("Groq LLM response (topic):", llm_response)
        try:
            return json.loads(llm_response)
        except Exception as parse_exc:
            # Return raw response if JSON parsing fails
            return {"error": f"Failed to parse LLM response: {parse_exc}", "raw_response": llm_response}
    except Exception as e:
        return {"error": f"Groq API error: {e}"}
