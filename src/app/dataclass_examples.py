from dataclasses import dataclass
from enum import Enum


class ProjectStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class AIProject:
    name: str
    technology: str
    days: int
    status: ProjectStatus
    description: str | None = None