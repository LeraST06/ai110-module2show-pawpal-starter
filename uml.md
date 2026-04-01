# PawPal+ UML Class Diagram

> Updated in Phase 6 to reflect the final implementation.

![UML Class Diagram](uml_final.png)

```mermaid
classDiagram
    class Owner {
        +String name
        +int available_minutes
        +add_pet(pet) None
        +get_pets() list
    }

    class Pet {
        +String name
        +String species
        +Owner owner
        +add_task(task) None
        +get_tasks() list
    }

    class Task {
        +String title
        +int duration_minutes
        +String priority
        +String preferred_time
        +String frequency
        +date due_date
        +bool completed
        +priority_value() int
        +mark_complete() None
        +next_occurrence() Task
    }

    class Scheduler {
        +Owner owner
        +int available_minutes
        +list scheduled_tasks
        +list skipped_tasks
        +sort_by_priority() list
        +sort_by_time() list
        +filter_tasks(pet_name, completed) list
        +detect_conflicts() list
        +complete_task(task) None
        +build_schedule() None
        +explain_plan() str
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "1" Owner : schedules for
    Task --> Task : next_occurrence()
```

## What changed from the initial design

| | Initial | Final |
|---|---|---|
| `Task.is_recurring` | `bool` | Replaced by `frequency` (`"daily"` / `"weekly"` / `None`) |
| `Task.due_date` | not present | Added — used by `next_occurrence()` with `timedelta` |
| `Task.next_occurrence()` | not present | Returns a new Task shifted by frequency interval |
| `Scheduler` input | `(pet, owner)` | `(owner)` only — collects tasks across all pets via `_all_tasks()` |
| `Scheduler → Pet` | direct relationship | Now indirect — accessed through `Owner.get_pets()` |
| New Scheduler methods | — | `sort_by_time()`, `filter_tasks()`, `complete_task()`, `detect_conflicts()` |
