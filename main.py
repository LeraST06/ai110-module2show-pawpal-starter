from pawpal_system import Owner, Pet, Task, Scheduler

# Set up owner with 90 minutes available today
jordan = Owner(name="Jordan", available_minutes=90)

# Create two pets
mochi = Pet(name="Mochi", species="dog", owner=jordan)
luna = Pet(name="Luna", species="cat", owner=jordan)
jordan.add_pet(mochi)
jordan.add_pet(luna)

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
mochi.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high"))
mochi.add_task(Task(title="Flea medication", duration_minutes=5, priority="medium", preferred_time="morning", is_recurring=True))
mochi.add_task(Task(title="Trick training", duration_minutes=20, priority="low"))

# Add tasks to Luna
luna.add_task(Task(title="Clean litter box", duration_minutes=10, priority="high"))
luna.add_task(Task(title="Brushing", duration_minutes=15, priority="medium"))
luna.add_task(Task(title="Playtime", duration_minutes=25, priority="low"))

# Build and print the schedule
scheduler = Scheduler(owner=jordan)
scheduler.build_schedule()
print(scheduler.explain_plan())
