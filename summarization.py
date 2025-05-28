import json
from groq import Groq

def summarize(text: str) -> dict:
    """
    Generates a concise summary and extracts actionable recommendations from the input text
    using the Groq LLM.

    Args:
        text (str): The feedback text to summarize.

    Returns:
        dict: {
            "summary": str,
            "action_items": List[str]
        }
        or an error message if summarization fails.
    """
    client = Groq()
    prompt = (
        "Summarize this feedback and list action items.\n"
        "Return ONLY valid JSON in this exact format:\n"
        '{\n  "summary": "concise summary",\n  "action_items": ["item1", "item2"]\n}\n'
        f"Text: {text}"
    )
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.0
        )
        llm_response = response.choices[0].message.content.strip()
        print("Groq LLM response (summary):", llm_response)
        try:
            return json.loads(llm_response)
        except Exception as parse_error:
            return {"error": f"Failed to parse LLM response: {parse_error}", "raw_response": llm_response}
    except Exception as api_error:
        return {"error": f"Groq API error: {api_error}"}
