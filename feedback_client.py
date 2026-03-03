import os
import json
import requests

class FeedbackClient:
    """Simple client to send session data to an external feedback API.

    Usage:
      - Provide `api_key` and `endpoint` when constructing, or set env vars
        `SHOOTING_FEEDBACK_API_KEY` and `SHOOTING_FEEDBACK_API_ENDPOINT`.
      - If no endpoint/key provided, client will return a helpful error.
    """

    def __init__(self, api_key: str | None = None, endpoint: str | None = None, timeout: int = 10):
        self.api_key = api_key or os.getenv("SHOOTING_FEEDBACK_API_KEY")
        # If endpoint not provided, allow defaulting to OpenAI Chat Completions
        self.endpoint = endpoint or os.getenv("SHOOTING_FEEDBACK_API_ENDPOINT")
        self.timeout = timeout

    def get_personalized_feedback(self, session_data: dict, history: list[dict] | None = None) -> dict:
        """Send session data and optional history to the external API and return the response.

        Returns a dict containing the API response or an `error` key on failure.
        """
        # If api_key missing, fail early
        if not self.api_key:
            return {"error": "Feedback API key not configured"}

        # If endpoint is not provided and key looks like an OpenAI key, use OpenAI ChatCompletion
        if not self.endpoint and isinstance(self.api_key, str) and self.api_key.startswith("sk-"):
            openai_endpoint = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            user_msg = f"Provide concise, actionable shooting feedback for this session and short drills. Session data: {json.dumps(session_data)}. History: {json.dumps(history or [])}"
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a shooting coach. Provide brief, actionable feedback and short drill suggestions based on the session data."},
                    {"role": "user", "content": user_msg}
                ],
                "temperature": 0.2,
                "max_tokens": 400
            }

            try:
                resp = requests.post(openai_endpoint, json=payload, headers=headers, timeout=self.timeout)
                try:
                    data = resp.json()
                except Exception:
                    data = {"status_code": resp.status_code, "text": resp.text}

                if resp.ok:
                    # Extract assistant content
                    try:
                        content = data['choices'][0]['message']['content']
                    except Exception:
                        content = data
                    return {"ok": True, "response": content}
                else:
                    return {"error": "API returned error", "status_code": resp.status_code, "response": data}

            except requests.exceptions.RequestException as exc:
                return {"error": "request_exception", "details": str(exc)}

        # Otherwise use generic endpoint
        if not self.endpoint:
            return {"error": "Feedback API endpoint not configured"}

        payload = {
            "session": session_data,
            "history": history or []
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=self.timeout)
            try:
                data = resp.json()
            except Exception:
                data = {"status_code": resp.status_code, "text": resp.text}

            if resp.ok:
                return {"ok": True, "response": data}
            else:
                return {"error": "API returned error", "status_code": resp.status_code, "response": data}

        except requests.exceptions.RequestException as exc:
            return {"error": "request_exception", "details": str(exc)}
