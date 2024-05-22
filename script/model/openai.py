from openai import OpenAI
from loguru import logger

from typing import Optional
from .base_model import BaseModel

class OpenaiModel(BaseModel):
    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__()
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.system_prompt = "You are a helpful assistant."
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.85,
        }

    def set_system_prompt(self, system_prompt: str):
        # todo: 添加 system prompt
        pass
    
    def set_generation_config(self, **kwargs):
        # todo: 设置 generation config
        pass
    
    def base_generate(self, input_content: str) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": input_content},
                ],
                stream=False,
                **self.generation_config
            )
            res = response.choices[0].message.content.strip()
            return res
        except KeyError as e:
            logger.error(f"KeyError occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
