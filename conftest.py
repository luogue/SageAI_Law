"""All repository pytest entry points receive a new temporary database."""
from backend.test_database_bootstrap import install

install()
