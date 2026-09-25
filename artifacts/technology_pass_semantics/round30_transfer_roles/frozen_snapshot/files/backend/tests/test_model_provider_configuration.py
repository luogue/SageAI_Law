"""Provider retirement, fail-closed transport, and credential redaction."""
import io
import json
import logging
from types import SimpleNamespace

import pytest
import requests
from model_settings import configuration
from reasoning import llm_client
from review_v2 import deepseek_transport, llm_semantic_reviewer
from secret_redaction import SecretFormatter


@pytest.fixture(autouse=True)
def isolated_model(monkeypatch):
    monkeypatch.setenv('DEEPSEEK_API_KEY', 'test-private-credential-123456')
    monkeypatch.setenv('DEEPSEEK_MODEL', 'deepseek-chat')
    monkeypatch.setattr(llm_client, 'circuit_breaker', llm_client.CircuitBreaker())
    monkeypatch.setattr(llm_client.time, 'sleep', lambda _: None)


def test_retired_environment_cannot_route_requests(monkeypatch):
    monkeypatch.setenv('DASHSCOPE_API_KEY', 'obsolete')
    monkeypatch.setenv('ARK_API_KEY', 'obsolete')
    monkeypatch.setenv('LLM_PRIORITY', 'doubao,qwen')
    calls = []
    def post(url, **kwargs):
        calls.append((url, kwargs['json']['model']))
        return SimpleNamespace(status_code=200, json=lambda: {'choices': [{'message': {'content': 'OK'}}]})
    monkeypatch.setattr(llm_client.requests, 'post', post)
    assert llm_client.call_llm('Reply OK') == 'OK'
    assert list(llm_client.MODEL_DEFINITIONS) == ['deepseek']
    assert calls == [('https://api.deepseek.com/v1/chat/completions', 'deepseek-chat')]
    assert llm_semantic_reviewer.get_llm_review_status()['configured_models'] == ['deepseek']
    monkeypatch.delenv('DEEPSEEK_API_KEY')
    assert not llm_semantic_reviewer.get_llm_review_status()['available']
    assert not llm_client._build_available_models()


def test_shared_configuration_and_environment_override(monkeypatch):
    monkeypatch.setenv('DEEPSEEK_MODEL', 'custom-model')
    assert configuration() == deepseek_transport.configuration()
    assert configuration()['key'] == 'test-private-credential-123456'
    assert configuration()['model'] == 'custom-model'


@pytest.mark.parametrize('status,attempts', [(401, 1), (429, 1), (400, 1), (503, 3)])
def test_provider_errors_never_fallback_or_publish_body(monkeypatch, caplog, status, attempts):
    calls = []
    def post(url, **kwargs):
        calls.append(url)
        return SimpleNamespace(status_code=status, text=configuration()['key'])
    monkeypatch.setattr(llm_client.requests, 'post', post)
    with pytest.raises(llm_client.AllModelsFailedError) as exc:
        llm_client.call_llm('test')
    assert len(calls) == attempts
    assert set(calls) == {configuration()['url']}
    assert configuration()['key'] not in caplog.text + str(exc.value)


def test_network_exception_does_not_expose_key(monkeypatch, caplog):
    def post(*args, **kwargs):
        raise requests.ConnectionError(configuration()['key'])
    monkeypatch.setattr(llm_client.requests, 'post', post)
    with pytest.raises(llm_client.AllModelsFailedError) as exc:
        llm_client.call_llm('test', max_retries=1)
    assert configuration()['key'] not in caplog.text + str(exc.value)


def test_success_content_and_fact_diagnostics_redact_credentials(monkeypatch):
    key = configuration()['key']
    response = SimpleNamespace(status_code=200, json=lambda: {'choices': [
        {'finish_reason': 'stop', 'message': {'content': json.dumps({'result': key})}}]})
    monkeypatch.setattr(llm_client.requests, 'post', lambda *a, **k: response)
    assert key not in llm_client.call_llm('test')
    body, payload = deepseek_transport.request_json('system', 'test', stage='TEST')
    assert key not in json.dumps([body, payload])
    invalid = SimpleNamespace(status_code=200, json=lambda: {'choices': [
        {'finish_reason': 'length', 'message': {'content': key}}]})
    with pytest.raises(deepseek_transport.FactExtractionError) as exc:
        deepseek_transport.model_json(invalid, 'TEST')
    assert key not in str(exc.value) + json.dumps(exc.value.diagnostics)


def test_log_formatter_redacts_arguments_and_tracebacks():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(SecretFormatter('%(message)s'))
    logger = logging.getLogger('credential-regression')
    logger.addHandler(handler)
    try:
        try:
            raise ValueError(configuration()['key'])
        except ValueError:
            logger.exception('credential=%s', configuration()['key'])
        assert configuration()['key'] not in stream.getvalue()
        assert '[REDACTED]' in stream.getvalue()
    finally:
        logger.removeHandler(handler)
