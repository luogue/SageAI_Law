"""Pytest compatibility hooks for legacy test modules."""

from __future__ import annotations

import builtins

# Also covers pytest launched with backend as its root directory.
try:
    from backend.test_database_bootstrap import install
except ModuleNotFoundError:
    from test_database_bootstrap import install
install()

from layers.validation_layer import ValidationLayer


builtins.ValidationLayer = ValidationLayer
