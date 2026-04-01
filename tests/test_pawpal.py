from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high"))
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium"))
    assert len(pet.get_tasks()) == 2
