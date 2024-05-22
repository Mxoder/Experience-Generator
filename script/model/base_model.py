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
