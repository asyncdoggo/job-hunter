from abc import ABC, abstractmethod


class ChatAPI:
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, message):
        pass



import google.generativeai as genai
class GeminiAPI(ChatAPI):
    def __init__(self, api_key, generation_config, model_name="gemini-1.5-flash"):
        self.api_key = api_key
        self.generation_config = generation_config
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name,
                                generation_config=generation_config)
        
    def get_response(self, message, file=None):
        prompt_parts = []
        
        if file:
            prompt_parts.append(genai.upload_file(file))
        prompt_parts.append(message)
        
        response = self.model.generate_content(prompt_parts)
        return response.text


