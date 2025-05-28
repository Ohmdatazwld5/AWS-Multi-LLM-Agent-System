from groq import Groq
import json

def extract(text: str) -> dict:
    """
    Extracts context-aware keywords with relevance scores
    Returns:
        {
            "keywords": [
                {"keyword": str, "relevance": 0.0-1.0},
                ...
            ]
        }
    """
    client = Groq()
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "user",
                "content": f"""Extract keywords from this text with relevance scores.
                Return JSON format:
                {{
                    "keywords": [
                        {{"keyword": "str", "relevance": 0.0-1.0}},
                        ...
                    ]
                }}
                Text: {text}"""
            }],
            temperature=0.4
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}