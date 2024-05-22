from pathlib import Path

# Get the current directory where this script is located
cur_dir = Path(__file__).resolve().parent   # config_dir
base_dir = cur_dir.parent
config_file = cur_dir / 'config.json'

data_dir = base_dir / 'data'

script_dir = base_dir / 'script'
model_dir = script_dir / 'model'
util_dir = script_dir / 'util'

prompt_dir = base_dir / 'prompt'
generator_prompt_file = prompt_dir / 'generator.md'
paraphraser_prompt_file = prompt_dir / 'paraphraser.md'
compressor_prompt_file = prompt_dir / 'compressor.md'
title_maker_prompt_file = prompt_dir / 'title_maker.md'

generated_dir = base_dir / 'generated'
