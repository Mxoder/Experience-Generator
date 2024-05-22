import json
from typing import Optional
from abc import ABC, abstractmethod

from config.config import (
    config_file,
    generator_prompt_file,
    paraphraser_prompt_file,
    compressor_prompt_file,
    title_maker_prompt_file
)

class BaseModel(ABC):
    def __init__(self):
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config_content = json.load(f)
        with open(generator_prompt_file, 'r', encoding='utf-8') as f:
            self.generator_prompt = f.read()
        with open(paraphraser_prompt_file, 'r', encoding='utf-8') as f:
            self.paraphraser_prompt = f.read()
        with open(compressor_prompt_file, 'r', encoding='utf-8') as f:
            self.compressor_prompt = f.read()
        with open(title_maker_prompt_file, 'r', encoding='utf-8') as f:
            self.title_maker_prompt = f.read()
    
    @abstractmethod
    def set_system_prompt(self, system_prompt: str):
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def set_generation_config(self, **kwargs):
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def base_generate(self, input_content: str) -> Optional[str]:
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def generate_text(self) -> Optional[str]:
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def paraphrase_text(self) -> Optional[str]:
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def compress_text(self) -> Optional[str]:
        raise NotImplementedError("Subclasses must implement the read_file method.")
    
    @abstractmethod
    def make_title(self) -> Optional[str]:
        raise NotImplementedError("Subclasses must implement the read_file method.")
