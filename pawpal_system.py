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
        mapping = {"high": 3, "medium": 2, "low": 1}
        return mapping.get(self.priority, 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str  # e.g. "dog", "cat"
    owner: "Owner" = field(repr=False)
    _tasks: list = field(default_factory=list, init=False, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self._tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self._tasks


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes  # total daily time budget
        self._pets: list = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet and ensure it points back to this owner."""
        pet.owner = self
        self._pets.append(pet)

    def get_pets(self) -> list:
        """Return all pets belonging to this owner."""
        return self._pets


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.available_minutes = owner.available_minutes
        self.scheduled_tasks: list = []
        self.skipped_tasks: list = []

    def _all_tasks(self) -> list:
        """Gather all tasks from all of the owner's pets."""
        tasks = []
        for pet in self.owner.get_pets():
            tasks.extend(pet.get_tasks())
        return tasks

    def sort_by_priority(self) -> list:
        """Return all tasks sorted by priority (highest first)."""
        return sorted(self._all_tasks(), key=lambda t: t.priority_value(), reverse=True)

    def build_schedule(self) -> None:
        """Greedily schedule tasks by priority until time runs out."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        remaining = self.available_minutes

        for task in self.sort_by_priority():
            if task.duration_minutes <= remaining:
                self.scheduled_tasks.append(task)
                remaining -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)

    def explain_plan(self) -> str:
        """Return a human-readable summary of the schedule."""
        if not self.scheduled_tasks and not self.skipped_tasks:
            return "No schedule built yet. Call build_schedule() first."

        lines = [f"Daily plan for {self.owner.name} ({self.available_minutes} min available)\n"]

        lines.append("Scheduled:")
        for task in self.scheduled_tasks:
            lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority} priority)")

        if self.skipped_tasks:
            lines.append("\nSkipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority} priority)")

        total = sum(t.duration_minutes for t in self.scheduled_tasks)
        lines.append(f"\nTotal scheduled: {total} min")
        return "\n".join(lines)
