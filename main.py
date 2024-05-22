import os
import json
from pathlib import Path
from loguru import logger

from config.config import generated_dir, config_file
from script.model.base_model import BaseModel
from script.model.ernie import ErnieModel
from script.model.openai import OpenaiModel
from script.util.file_reader import FileReader

GENERATED_TEMPLATE = "## {}\n\n{}"

def ensure_directory_exists(directory: Path):
    """Ensure that the directory exists. If not, create it."""
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"An error occurred while creating the directory {directory}: {e}")
        raise

def write_final_generated_text(raw_title: str, title: str, text: str, model: BaseModel):
    """Writes the generated text to the final markdown file."""
    try:
        # Ensure generated_dir exists
        ensure_directory_exists(generated_dir)
        final_generated_text = GENERATED_TEMPLATE.format(title, text)
        target_path = generated_dir / f'{raw_title.replace("/", "-")}-{model.__class__.__name__}.md'
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(final_generated_text)
        logger.info(f'Successfully generated and saved to: {target_path}')
    except Exception as e:
        logger.error(f"An error occurred while writing the final generated text: {e}")

def main(model: BaseModel):
    """Main function to run the model and write the outputs."""
    try:
        file_reader = FileReader()
        ref_texts = file_reader.get_extracted_text()
        for title, content in ref_texts.items():
            generated_text = model.generate_text(content)
            paraphrased_text = model.paraphrase_text(generated_text)
            compressed_text = model.compress_text(content, paraphrased_text)
            made_title = model.make_title(content, paraphrased_text)

            write_final_generated_text(title, made_title, compressed_text, model)
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")

if __name__ == '__main__':
    try:
        # Read configuration
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Determine which model to use based on configuration
        chosen_model = config.get('chosen_model').lower()
        
        if chosen_model == 'ernie':
            model = ErnieModel(**config['ernie'])
            logger.info("Ernie Model selected based on configuration.")
        elif chosen_model == 'openai':
            model = OpenaiModel(**config['openai'])
            logger.info("OpenAI Model selected based on configuration.")
        else:
            raise ValueError(f"Chosen model '{chosen_model}' in config.json is not supported.")

        # Run main function with the selected model
        main(model)

    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
    except json.JSONDecodeError:
        logger.error(f"Config file is not valid JSON: {config_file}")
    except ValueError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"Failed to execute the script: {e}")
