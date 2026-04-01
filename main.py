from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

jordan = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", owner=jordan)
luna = Pet(name="Luna", species="cat", owner=jordan)
jordan.add_pet(mochi)
jordan.add_pet(luna)

mochi.add_task(Task(title="Morning walk",    duration_minutes=30, priority="high",   preferred_time="07:00", frequency="daily",  due_date=date.today()))
mochi.add_task(Task(title="Feed breakfast",  duration_minutes=10, priority="high",   preferred_time="07:30", frequency="daily",  due_date=date.today()))
mochi.add_task(Task(title="Flea medication", duration_minutes=5,  priority="medium", preferred_time="08:00", frequency="weekly", due_date=date.today()))
mochi.add_task(Task(title="Trick training",  duration_minutes=20, priority="low"))

luna.add_task(Task(title="Clean litter box", duration_minutes=10, priority="high",   preferred_time="09:00", frequency="daily",  due_date=date.today()))
luna.add_task(Task(title="Brushing",         duration_minutes=15, priority="medium", preferred_time="17:00"))
# Intentional conflict: same time as Mochi's morning walk
luna.add_task(Task(title="Morning feeding",  duration_minutes=5,  priority="high",   preferred_time="07:00"))

scheduler = Scheduler(owner=jordan)
scheduler.build_schedule()

print("=== Today's Schedule ===")
print(scheduler.explain_plan())

print("\n=== Conflict Check ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

print("\n--- Completing 'Morning walk' (daily recurring) ---")
morning_walk = mochi.get_tasks()[0]
scheduler.complete_task(morning_walk)
next_walk = mochi.get_tasks()[-1]
print(f"Next occurrence: '{next_walk.title}' due {next_walk.due_date}")

print("\n--- Completing 'Flea medication' (weekly recurring) ---")
flea_med = mochi.get_tasks()[2]
scheduler.complete_task(flea_med)
next_flea = mochi.get_tasks()[-1]
print(f"Next occurrence: '{next_flea.title}' due {next_flea.due_date}")
