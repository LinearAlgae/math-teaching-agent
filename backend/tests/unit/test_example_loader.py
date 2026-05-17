import pytest

from src.services.example_loader import ResourceRetriever


@pytest.fixture
def loader():
    return ResourceRetriever()


def test_example_loader_initialization(loader):
    assert loader.resources_dir.name == "markdown_output"


def test_get_examples_for_subject_returns_list(loader):
    examples = loader.get_examples_for_subject("logarithm", max_chars=6000)
    assert isinstance(examples, list)
