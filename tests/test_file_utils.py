import json
from pathlib import Path

import pytest

from src.app.file_utils import (
    load_models_from_csv,
    load_models_from_json,
    save_models_to_csv,
    save_models_to_json,
)


# test loading data from json file
def test_load_models_from_json():
    path = Path("data/models.json")

    models = load_models_from_json(path)

    assert len(models) >= 3
    assert models[0]["name"] == "GPT"
    assert models[0]["provider"] == "OpenAI"


# test loading data from csv file
def test_load_models_from_csv():
    path = Path("data/models.csv")

    models = load_models_from_csv(path)

    assert len(models) >= 3
    assert models[0]["name"] == "GPT"
    assert models[0]["provider"] == "OpenAI"


# test json saving
def test_save_models_to_json(tmp_path):
    path = tmp_path / "models.json"

    models = [{"name": "TestGPT", "provider": "TestProvider"}]

    save_models_to_json(path, models)

    loaded_models = load_models_from_json(path)

    assert loaded_models == models


# test csv saving
def test_save_models_to_csv(tmp_path):
    path = tmp_path / "models.csv"

    models = [{"name": "TestGPT", "provider": "TestProvider"}]

    save_models_to_csv(path, models)

    loaded_models = load_models_from_csv(path)

    assert loaded_models == models


def test_load_models_from_json_file_not_found():
    path = Path("data/does_not_exist.json")

    with pytest.raises(FileNotFoundError):
        load_models_from_json(path)


def test_load_models_from_json_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"

    path.write_text('{"name": "GPT", "provider": "OpenAI"', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_models_from_json(path)
