"""Family-independent DeepSeek JSON transport, without provider fallback."""
import json
import os
from pathlib import Path
import re
import requests
from review_v2.fact_validation import FactExtractionError


def configuration():
    from model_settings import configuration as shared_configuration
    return shared_configuration()


def model_json(response, stage):
    if response.status_code != 200:
        raise FactExtractionError(f'DEEPSEEK_HTTP_{response.status_code}', failed_stage=stage+'_TRANSPORT',
                                  field='http.status', actual=response.status_code, expected=200, repairable=False)
    content = None
    try:
        from secret_redaction import redact_secrets
        body = redact_secrets(response.json())
        choice = body['choices'][0]
        content = choice['message']['content']
        if choice.get('finish_reason') != 'stop':
            raise FactExtractionError('DEEPSEEK_INCOMPLETE_JSON', failed_stage=stage+'_JSON',
                field='finish_reason', model_raw_value=content, actual=choice.get('finish_reason'), expected='stop')
        if not isinstance(content, str):
            raise ValueError('expected JSON string')
        payload = re.sub(r'^```(?:json)?\s*\n([\s\S]*?)\n```$', r'\1', content.strip(), flags=re.I)
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError('expected JSON object')
        return body, data
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        raise FactExtractionError('INVALID_MODEL_JSON', failed_stage=stage+'_JSON', field='message.content',
            model_raw_value=content, actual=type(exc).__name__, expected='complete JSON object') from exc


def request_json(system, payload, *, stage, config=None):
    config = configuration() if config is None else config
    if not config['key']:
        raise FactExtractionError('DEEPSEEK_NOT_CONFIGURED', failed_stage='CONFIGURATION', field='provider', repairable=False)
    try:
        response = requests.post(config['url'], headers={'Authorization': 'Bearer ' + config['key']},
            json={'model': config['model'], 'temperature': 0, 'max_tokens': 8192,
                'response_format': {'type': 'json_object'},
                'messages': [{'role': 'system', 'content': system},
                             {'role': 'user', 'content': payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)}]},
            timeout=(10, 180))
        return model_json(response, stage)
    except requests.RequestException as exc:
        raise FactExtractionError('DEEPSEEK_REQUEST_FAILED:' + type(exc).__name__,
            failed_stage=stage + '_TRANSPORT', field='http.response', repairable=False) from None
