from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    preferred_time: Optional[str] = None   # "HH:MM" format, e.g. "08:00"
    frequency: Optional[str] = None        # "daily", "weekly", or None (one-off)
    due_date: Optional[date] = None        # date this task is due
    completed: bool = False

    def priority_value(self) -> int:
        """Return numeric priority so tasks can be sorted (high=3, medium=2, low=1)."""
        mapping = {"high": 3, "medium": 2, "low": 1}
        return mapping.get(self.priority, 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Return a new Task scheduled for the next occurrence based on frequency."""
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            raise ValueError(f"Task '{self.title}' has no frequency set — cannot recur.")

        next_due = (self.due_date or date.today()) + delta
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            due_date=next_due,
            completed=False,
        )


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

    def _pet_for_task(self, task: Task) -> Optional[Pet]:
        """Find which pet owns a given task."""
        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                return pet
        return None

    def sort_by_priority(self) -> list:
        """Return all tasks sorted by priority (highest first)."""
        return sorted(self._all_tasks(), key=lambda t: t.priority_value(), reverse=True)

    def sort_by_time(self) -> list:
        """Return all tasks sorted by preferred_time (HH:MM), tasks without a time go last."""
        return sorted(
            self._all_tasks(),
            key=lambda t: t.preferred_time if t.preferred_time else "99:99"
        )

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> list:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = []
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                tasks.append(task)
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any scheduled tasks that share the same preferred_time."""
        warnings = []
        seen: dict[str, Task] = {}
        for task in self.scheduled_tasks:
            if not task.preferred_time:
                continue
            if task.preferred_time in seen:
                other = seen[task.preferred_time]
                warnings.append(
                    f"Conflict at {task.preferred_time}: '{other.title}' and '{task.title}' overlap."
                )
            else:
                seen[task.preferred_time] = task
        return warnings

    def complete_task(self, task: Task) -> None:
        """Mark a task complete; if it recurs, add the next occurrence to the same pet."""
        task.mark_complete()
        if task.frequency:
            pet = self._pet_for_task(task)
            if pet:
                pet.add_task(task.next_occurrence())

    def build_schedule(self) -> None:
        """Schedule incomplete tasks sorted by preferred_time then priority; skip tasks that don't fit."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        remaining = self.available_minutes

        candidates = [t for t in self._all_tasks() if not t.completed]
        sorted_tasks = sorted(
            candidates,
            key=lambda t: (t.preferred_time if t.preferred_time else "99:99", -t.priority_value())
        )

        for task in sorted_tasks:
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
            time_label = f" at {task.preferred_time}" if task.preferred_time else ""
            recur_label = f" [{task.frequency}]" if task.frequency else ""
            lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority}{time_label}{recur_label})")

        if self.skipped_tasks:
            lines.append("\nSkipped (not enough time):")
            for task in self.skipped_tasks:
                flag = "  *** HIGH PRIORITY — consider freeing up time!" if task.priority == "high" else ""
                lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority}){flag}")

        total = sum(t.duration_minutes for t in self.scheduled_tasks)
        lines.append(f"\nTotal scheduled: {total} min")
        return "\n".join(lines)
