import requests 

class OllamaLLM:
    def __init__(self, model="mistral"):
        self.model = model 
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=payload) 
        response.raise_for_status() 

        return response.json()["response"]