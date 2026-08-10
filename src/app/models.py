from dataclasses import dataclass

@dataclass
class Person:
    name: str
    birth_year: int

    def calculate_age(self, current_year: int) -> int:
        return current_year - self.birth_year

    def introduce(self) -> str:
        return f"My name is {self.name}."

class AIModel:
    def __init__(self, name: str, provider: str):
        self.name = name
        self.provider = provider

    def describe(self) -> str:
        return f"{self.name} is provided by {self.provider}."
