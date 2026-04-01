from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    preferred_time: Optional[str] = None  # e.g. "morning", "evening"
    is_recurring: bool = False
    completed: bool = False

    def priority_value(self) -> int:
        """Return numeric priority so tasks can be sorted (high=3, medium=2, low=1)."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str  # e.g. "dog", "cat"
    owner: "Owner" = field(repr=False)
    _tasks: list = field(default_factory=list, init=False, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes  # total daily time budget
        self._pets: list = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass

    def get_pets(self) -> list:
        """Return all pets belonging to this owner."""
        pass


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.available_minutes = owner.available_minutes
        self.scheduled_tasks: list = []
        self.skipped_tasks: list = []

    def sort_by_priority(self) -> list:
        """Return tasks sorted by priority (highest first)."""
        pass

    def detect_conflicts(self) -> list:
        """Return tasks that exceed the remaining time budget."""
        pass

    def build_schedule(self) -> None:
        """Select and order tasks that fit within the available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable summary of the schedule."""
        pass
