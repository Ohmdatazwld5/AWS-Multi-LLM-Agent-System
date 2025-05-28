from groq import Groq

def summarize(text: str) -> dict:
    """
    Generates concise summary and actionable recommendations
    Returns:
        {
            "summary": str,
            "action_items": List[str]
        }
    """
    client = Groq()
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "user",
                "content": f"""Summarize this feedback and list action items.
                Format: {{
                    "summary": "concise summary",
                    "action_items": ["item1", "item2"]
                }}
                Text: {text}"""
            }],
            temperature=0.5
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}