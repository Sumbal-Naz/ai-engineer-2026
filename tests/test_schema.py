import pytest
from pydantic import ValidationError

from src.app.schemas import AIModelRequest


def test_model_request_strips_whitespace():
    model = AIModelRequest(name="  GPT  ", provider="  OpenAI  ")

    assert model.name == "GPT"
    assert model.provider == "OpenAI"


def test_model_request_rejects_blank_name():
    with pytest.raises(ValidationError):
        AIModelRequest(name="   ", provider="OpenAI")


def test_model_request_rejects_blank_provider():
    with pytest.raises(ValidationError):
        AIModelRequest(name="GPT", provider="   ")
