import json
import requests
from typing import Optional
from .base_model import BaseModel
from loguru import logger

class ErnieModel(BaseModel):
    def __init__(self, api_key: str, secret_key: str, model: str):
        """
        Initializes the ERNIE model with necessary credentials and default settings.

        :param api_key: The API key for accessing the ERNIE service.
        :param secret_key: The secret key associated with the API key.
        :param model: The name or identifier of the ERNIE model to use.
        """
        super().__init__()
        self.api_key = api_key
        self.secret_key = secret_key
        self.model_name = model
        self.access_token = self._get_access_token()
        self.system_prompt = None
        self.temperature = 0.9
        self.top_p = 0.8

    def set_system_prompt(self, system_prompt: str):
        """
        Sets the system-level prompt that influences the model's behavior across all generations.

        :param system_prompt: The system-level prompt string.
        """
        self.system_prompt = system_prompt

    def set_generation_config(
        self,
        temperature: Optional[float] = 0.9,
        top_p: Optional[float] = 0.8
    ):
        """
        Adjusts the generation parameters controlling output randomness and diversity.

        :param temperature: Float value controlling randomness; defaults to 0.9.
        :param top_p: Float value for nucleus sampling; defaults to 0.8.
        """
        self.temperature = temperature
        self.top_p = top_p

    def base_generate(self, input_content: str) -> Optional[str]:
        """
        Core method to send a request to the ERNIE model and receive generated text.

        :param input_content: The content to be processed by the model.
        :return: Generated text from the model or None on failure.
        """
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
    
    def _get_access_token(self) -> Optional[str]:
        """
        Retrieves an access token required for authenticated API calls to the ERNIE service.

        :return: Access token string on success, None on failure.
        """
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
