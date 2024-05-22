from typing import Optional
from .base_model import BaseModel

class OpenaiModel(BaseModel):
    def __init__(self):
        super().__init__()

    def set_system_prompt(self, system_prompt: str):
        return super().set_system_prompt(system_prompt)
    
    def set_generation_config(self, **kwargs):
        return super().set_generation_config(**kwargs)
    
    def base_generate(self, input_content: str) -> Optional[str]:
        return super().base_generate(input_content)
    
    def generate_text(self) -> Optional[str]:
        pass
    
    def paraphrase_text(self) -> Optional[str]:
        pass
    
    def compress_text(self) -> Optional[str]:
        return super().compress_text()
    
    def make_title(self) -> Optional[str]:
        return super().make_title()
