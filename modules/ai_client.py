# ══════════════════════════════════════════════════════
#  ai_client.py
#  Handles all Claude AI API connections
#  Used by every other AI module in the project
# ══════════════════════════════════════════════════════

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

def ask_claude(prompt, max_tokens=1000):
    """
    Sends a prompt to Claude and returns the response text.
    This is the core function all AI features use.
    """
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


def test_ai_connection():
    """
    Tests the Claude API connection.
    Run this file directly to verify everything is working.
    """
    try:
        response = ask_claude(
            "You are a NZ business advisor. In one sentence, "
            "what is the most important financial ratio for an NZ SME owner to monitor?"
        )
        print("✓ Claude AI connected successfully")
        print(f"✓ Response: {response}")
    except Exception as e:
        print(f"✗ AI connection failed: {e}")


if __name__ == "__main__":
    test_ai_connection()