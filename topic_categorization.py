from groq import Groq
import json

def categorize(text: str) -> dict:
    """
    Categorizes feedback into predefined topics
    Returns:
        {
            "primary_topic": str,
            "secondary_topics": List[str],
            "confidence": 0.0-1.0
        }
    """
    client = Groq()
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "user",
                "content": f"""Categorize this text using these topics: 
                [Product Quality, Delivery, Support, Pricing, Features, Other].
                Return JSON format:
                {{
                    "primary_topic": "category",
                    "secondary_topics": ["category1", "category2"],
                    "confidence": 0.0-1.0
                }}
                Text: {text}"""
            }],
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}