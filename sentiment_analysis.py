import json
from groq import Groq

def analyze(text: str) -> dict:
    """
    Analyzes the sentiment of the input text using the Groq LLM.
    The result includes the sentiment label ('positive', 'negative', or 'neutral')
    and a confidence score between 0.0 and 1.0.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: Sentiment analysis result, or error details if parsing fails.
    """
    client = Groq()
    prompt = (
        "Analyze the sentiment of this text as 'positive', 'negative', or 'neutral'.\n"
        "Return only valid JSON and nothing else. Example:\n"
        "{\n"
        '  "sentiment": "positive|negative|neutral",\n'
        '  "confidence": 0.0-1.0\n'
        "}\n"
        f"Text: {text}"
    )
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        llm_output = response.choices[0].message.content
        print("Groq LLM response (sentiment):", llm_output)
        return json.loads(llm_output)
    except Exception as e:
        # Log the raw output for troubleshooting
        raw = response.choices[0].message.content if 'response' in locals() else None
        print("Error parsing LLM output:", e, "Raw output:", raw)
        return {"error": str(e), "raw_output": raw}
