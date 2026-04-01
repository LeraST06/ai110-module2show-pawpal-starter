# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care planning app built with Python and Streamlit. It helps busy pet owners build a realistic daily care schedule based on task priority, time constraints, and preferred care times.

## 📸 Demo

**Owner & pet setup**
<a href="/course_images/ai110/pawpal_screenshot1.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot1.png' title='PawPal App - Setup' width='' alt='PawPal App Setup' class='center-block' /></a>

**Task management**
<a href="/course_images/ai110/pawpal_screenshot2.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot2.png' title='PawPal App - Tasks' width='' alt='PawPal App Tasks' class='center-block' /></a>

**Generated daily schedule with conflict warning**
<a href="/course_images/ai110/pawpal_screenshot3.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot3.png' title='PawPal App - Schedule' width='' alt='PawPal App Schedule' class='center-block' /></a>

## Features

- **Owner & pet setup** — enter your name, your pet's name and species, and how many minutes you have available today
- **Task management** — add care tasks (walks, feeding, meds, grooming, etc.) with duration, priority, preferred time, and repeat frequency
- **Priority-first scheduling** — tasks are sorted high → medium → low and greedily fit into your time budget; anything that doesn't fit is flagged
- **Time-aware ordering** — tasks with a preferred time (HH:MM) are placed before unscheduled tasks and sorted chronologically
- **Conflict detection** — the scheduler warns you if two tasks share the same preferred time slot
- **Recurring tasks** — daily and weekly tasks automatically queue their next occurrence when completed, using Python's `timedelta`
- **Skipped task warnings** — high-priority tasks that don't fit due to time constraints are highlighted in red

## Project Structure

```
pawpal_system.py   # backend logic — Owner, Pet, Task, Scheduler classes
app.py             # Streamlit UI
main.py            # CLI demo script
tests/             # pytest test suite
uml.md             # final UML class diagram (Mermaid.js)
reflection.md      # design and AI collaboration reflection
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

To run the CLI demo:

```bash
python3 main.py
```

To run tests:

```bash
python3 -m pytest tests/
```
