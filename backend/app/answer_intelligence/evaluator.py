import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRACTICE_QUESTION = "Tell me about a project you've worked on."


def evaluate_answer(question: str, answer: str) -> dict:
    prompt = f"""You are an interview coach evaluating a candidate's answer.

Question: {question}
Candidate's answer: {answer}

Evaluate this answer against the STAR format (Situation, Task, Action, Result).
Respond ONLY with valid JSON in this exact shape, no other text:

{{
  "star_present": false,
  "strengths": ["..."],
  "improvements": ["..."],
  "suggested_focus": "..."
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        cleaned = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        return parsed

    except Exception as e:
        print(f"Answer evaluation failed: {e}")
        return {
            "star_present": None,
            "strengths": [],
            "improvements": [],
            "suggested_focus": "Evaluation unavailable.",
        }


if __name__ == "__main__":
    result = evaluate_answer(
        PRACTICE_QUESTION,
        "I made an app using Python."
    )
    print(json.dumps(result, indent=2))