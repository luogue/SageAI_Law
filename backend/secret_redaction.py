"""Redact credentials at model and logging output boundaries."""
import logging
import os
import re


def redact_secrets(value):
    if isinstance(value, dict):
        return {key: redact_secrets(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    if not isinstance(value, str):
        return value
    for name, secret in os.environ.items():
        if name.endswith(('_API_KEY', '_SECRET_KEY', '_ACCESS_KEY_SECRET')) and len(secret) >= 8:
            value = value.replace(secret, '[REDACTED]')
    return re.sub(r'(?i)\bsk-[a-z0-9_-]{8,}', '[REDACTED]', value)


class SecretFormatter(logging.Formatter):
    def format(self, record):
        return redact_secrets(super().format(record))
