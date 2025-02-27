import os
from groq import Groq, APIError
import httpx  

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

async def get_completion(prompt, model="llama-3.3-70b-versatile"):
    messages = [{"role": "user", "content": prompt}]
    
    try:
        chat_completion = await client.chat.completions.create_async(
            messages=messages,
            model=model,
        )
        return chat_completion.choices[0].message.content

    except APIError as e:
        return f"API error: {e}"
    except httpx.HTTPError as e:
        return f"Network error: {e}"
    except TimeoutError:
        return "Request timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"