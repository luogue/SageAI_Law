"""Pytest compatibility hooks for legacy test modules."""

from __future__ import annotations

import builtins

from layers.validation_layer import ValidationLayer


builtins.ValidationLayer = ValidationLayer
