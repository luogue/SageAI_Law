"""Single supported provider; process environment overrides backend/.env."""
import os
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent / '.env'
load_dotenv(ENV_FILE, override=False)

MODEL_DEFINITIONS = {
    'deepseek': {
        'name': 'DeepSeek', 'provider': 'deepseek',
        'api_key_env': 'DEEPSEEK_API_KEY',
        'model_env': 'DEEPSEEK_MODEL', 'default_model': 'deepseek-chat',
        'url': 'https://api.deepseek.com/v1/chat/completions',
        'max_tokens': 8192, 'temperature': 0.1,
    },
}


def configuration():
    definition = MODEL_DEFINITIONS['deepseek']
    return {'key': os.getenv('DEEPSEEK_API_KEY', '').strip(),
            'model': os.getenv('DEEPSEEK_MODEL', '').strip() or definition['default_model'],
            'url': definition['url']}
