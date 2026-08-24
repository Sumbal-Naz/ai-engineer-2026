from pathlib import Path
import json
import csv

def get_data_path(filename: str) -> Path:
    return Path("data") / filename

def load_models_from_json(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_models_to_json(file_path: Path, models: list[dict]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(models, file, indent=4)

def load_models_from_csv(file_path: Path) -> list[dict]:
    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_models_to_csv(file_path: Path, models: list[dict]) -> None:
    with file_path.open("w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["name", "provider"]
        )

        writer.writeheader()
        writer.writerows(models)

"""
def write_text_file(path: Path, content: str)  -> None:
    path.write_text(content, encoding="utf-8")


file_path = Path("data") / "example.txt"

file_path.write_text("AI Engineer 2026", encoding="utf-8")

content = file_path.read_text(encoding="utf-8")
print(content)
"""

if __name__ == "__main__":

    
    json_path = get_data_path("models.json")
    json_models = load_models_from_json(json_path)

    print(json_models)

    json_models.append(
        {
            "name": "Gemini",
            "provider": "Google"
        }
    )

    save_models_to_json(json_path, json_models)

    print("Models saved successfully.")
    
    csv_path = get_data_path("models.csv")
    csv_models = load_models_from_csv(csv_path)

    csv_models.append(
        {
            "name": "Gemini",
            "provider": "Google"
        }
    )

    save_models_to_csv(csv_path, csv_models)

    print("CSV saved successfully.")
