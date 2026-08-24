from src.app.models import AIModel

def test_AIModel():
    model = AIModel(
        name="GPT",
        provider="OpenAI"
    )

    assert model.name == "GPT"
    assert model.provider == "OpenAI"
    assert model.describe() == "GPT is provided by OpenAI."