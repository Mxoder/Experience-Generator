import json
import requests
from typing import Optional
from .base_model import BaseModel
from loguru import logger

class ErnieModel(BaseModel):
    def __init__(self, api_key: str, secret_key: str, model: str):
        super().__init__()
        self.api_key = api_key
        self.secret_key = secret_key
        self.model_name = model
        self.access_token = self._get_access_token()
        self.system_prompt = ""
        self.temperature = 0.9
        self.top_p = 0.8

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def set_generation_config(self, temperature: Optional[float] = 0.9, top_p: Optional[float] = 0.8):
        self.temperature = temperature
        self.top_p = top_p

    def base_generate(self, input_content: str) -> Optional[str]:
        base_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model_name}"
        url = f"{base_url}?access_token={self.access_token}"
        payload = json.dumps({
            "system": self.system_prompt,
            "messages": [{"role": "user", "content": input_content}],
            "temperature": self.temperature,
            "top_p": self.top_p,
        })
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            result = response.json().get('result')
            if result:
                return result
            else:
                logger.error(f"No result found in the response: {response.json()}")
                return None
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def generate_text(self, ref_text: str) -> Optional[str]:
        input_content = self.generator_prompt
        input_content = input_content.replace(r'{{ref_text}}', ref_text)
        return self.base_generate(input_content)
    
    def paraphrase_text(self, raw_text: str) -> Optional[str]:
        split_text = [text for text in raw_text.split('\n') if len(text.strip()) > 1]
        if len(split_text[0]) <= 40:
            split_text = split_text[1:]
        new_raw_text = '\n\n'.join(split_text)
        new_text = []
        i = 1
        accumulated_text = []
        for text in split_text:
            if len(text) < 40:  # maybe the title
                # new_text.append(text)
                continue
            accumulated_text.append(text)
            if i % 3 == 0:
                input_content = self.paraphraser_prompt
                input_content = input_content.replace(r'{{raw_text}}', new_raw_text)
                input_content = input_content.replace(r'{{text_to_paraphrase}}', '\n'.join(accumulated_text))
                paraphrased_text = self.base_generate(input_content)
                new_text.append(paraphrased_text)
                accumulated_text = []
            i += 1
        if accumulated_text:
            new_text.extend(accumulated_text)
        return '\n'.join(new_text)
    
    def compress_text(self, ref_text: str, raw_text: str) -> Optional[str]:
        input_content = self.compressor_prompt
        input_content = input_content.replace(r'{{ref_text}}', ref_text)
        input_content = input_content.replace(r'{{raw_text}}', raw_text)
        return self.base_generate(input_content)
    
    def make_title(self, ref_text: str, raw_text: str) -> Optional[str]:
        input_content = self.title_maker_prompt
        input_content = input_content.replace(r'{{ref_text}}', ref_text)
        input_content = input_content.replace(r'{{raw_text}}', raw_text)
        return self.base_generate(input_content)
    
    def _get_access_token(self) -> Optional[str]:
        url = f"https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        headers = {'Accept': 'application/json'}

        try:
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            if not access_token:
                logger.error("Failed to retrieve access token")
                return None
            return access_token
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve access token: {e}")
            return None
