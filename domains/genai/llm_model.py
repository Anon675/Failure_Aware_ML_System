import requests

class LLMModel:
    """
    Wrapper for local Ollama LLM.
    """

    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt, temperature=0.7):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        result = response.json()

        text = result.get("response", "")

        return text.strip()
