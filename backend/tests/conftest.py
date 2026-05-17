import pytest


@pytest.fixture
def sample_messages():
    return [
        {"role": "user", "content": "What is a logarithm?"},
        {"role": "assistant", "content": "A logarithm is..."},
    ]
