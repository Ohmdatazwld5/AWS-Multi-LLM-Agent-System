import json
from groq import Groq

def extract(text: str) -> dict:
    """
    Extracts keywords from the provided text using Groq LLM.
    Each keyword has an associated relevance score between 0.0 and 1.0.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary with a "keywords" list, or an error message if extraction fails.
    """
    client = Groq()
    prompt = (
        "Extract keywords from this text with relevance scores.\n"
        "Return ONLY valid JSON in this exact format:\n"
        '{\n  "keywords": [\n    {"keyword": "str", "relevance": 0.0-1.0},\n    ...\n  ]\n}\n'
        f"Text: {text}"
    )
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        llm_response = response.choices[0].message.content.strip()
        print("Groq LLM response (keywords):", llm_response)
        try:
            return json.loads(llm_response)
        except Exception as parse_error:
            return {"error": f"Failed to parse LLM response: {parse_error}", "raw_response": llm_response}
    except Exception as api_error:
        return {"error": f"Groq API error: {api_error}"}
