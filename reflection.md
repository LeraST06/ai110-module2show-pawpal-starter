# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three things a user needs to be able to do:
- Add their info and their pet (name, species, how much time they have per day)
- Add care tasks (walk, meds, grooming, etc.) with a duration and priority
- Generate a daily schedule that fits tasks into available time, highest priority first

Four classes:

**Owner** - name, available minutes per day; can add/get pets

**Pet** - name, species, linked to an owner; holds a list of tasks

**Task** - title, duration, priority (low/medium/high), optional preferred time, recurring flag; can return a numeric priority for sorting

**Scheduler** - takes a pet and builds the day's plan; sorts by priority, skips tasks that don't fit, explains what was scheduled and what wasn't

See [uml.md](uml.md) for the class diagram.

**b. Design changes**

- `Owner.add_pet()` now also sets `pet.owner = self` to keep both sides of the relationship in sync
- `Scheduler` was redesigned to take only `Owner` instead of `(pet, owner)`. It collects tasks from all pets via `_all_tasks()`, making it the true brain across the whole system
- `is_recurring: bool` was replaced by `frequency: str` ("daily"/"weekly"/None) and `due_date`. Recurring tasks now use `timedelta` to queue the next occurrence automatically when completed
- `detect_conflicts()` was initially folded into `build_schedule()`, then split back out as a post-build warning scanner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- Time budget (`available_minutes`) - tasks that don't fit are skipped entirely
- Priority (high/medium/low) - higher priority tasks are scheduled first
- Preferred time (`HH:MM`) - tasks with a set time are placed before unscheduled ones
- Completion status - already-done tasks are excluded from the daily build

Time budget was the most important constraint because without it, the scheduler has nothing to optimize against. Priority came next since the whole point is making sure the most critical care happens first.

**b. Tradeoffs**

Conflict detection only flags tasks with the exact same `preferred_time` string. A 30-minute task at `07:00` and a task at `07:15` won't trigger a warning even though they clearly overlap in real time.

This is reasonable for now because the app doesn't track actual start/end times. It only knows preferred time windows. Adding duration-aware overlap detection would require a proper time arithmetic layer, which is more complexity than the project needs at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

- Brainstorming classes and responsibilities before writing any code
- Generating class skeletons from the UML description
- Reviewing the skeleton for design issues (caught the Pet-Owner sync problem and the detect_conflicts overlap)
- Suggesting algorithmic improvements like a Pythonic rewrite of `filter_tasks`

The most useful prompts were specific ones: "review this skeleton for missing relationships" and "how should the Scheduler retrieve tasks across all pets?" (open-ended questions about design, not just "write me code.")

Keeping separate chat sessions for design (Phase 1), implementation (Phase 2), and algorithms (Phase 4) helped a lot. Each session stayed focused and didn't get confused by context from a different phase.

**b. Judgment and verification**

AI suggested replacing `filter_tasks` with a nested list comprehension. It is shorter, but harder to read at a glance. I kept the explicit loop version because the filtering logic is clearer that way, and readability matters more than line count for a teaching project.

I also rejected the original skeleton's `detect_conflicts()` as a separate method. AI generated it as standalone, but I recognized that running it separately from `build_schedule()` would mean tracking remaining time twice. I folded the logic in, then later brought `detect_conflicts()` back as a post-build warning scanner.

---

## 4. Testing and Verification

**a. What you tested**

- `mark_complete()` actually sets `completed = True`
- `add_task()` increases the pet's task count

These were the two most foundational behaviors. If marking tasks complete or adding tasks silently broke, everything built on top (filtering, scheduling, recurring logic) would give wrong results with no obvious error.

**b. Confidence**

Fairly confident in the core scheduling logic. The CLI demo in `main.py` covers the happy path well and the output matched expectations. Less confident in edge cases:
- What happens if `available_minutes` is 0?
- What if all tasks have the same priority and time?
- Does `next_occurrence()` behave correctly if `due_date` is None?

---

## 5. Reflection

**a. What went well**

The CLI-first workflow. Building and verifying `main.py` before touching Streamlit meant the backend logic was solid before worrying about the UI. Every bug was caught in the terminal where it was easy to debug.

**b. What you would improve**

Conflict detection. Right now it only catches exact `preferred_time` matches. A real pet owner could have a 30-minute walk at 07:00 and a feeding at 07:15 and that overlap wouldn't be flagged. Adding duration-aware conflict detection with proper time arithmetic would make the scheduler genuinely useful.

I'd also add a way to mark tasks complete directly in the Streamlit UI, so recurring tasks actually queue their next occurrence through the app, not just in the CLI.

**c. Key takeaway**

AI is fast at generating structure but it doesn't know your design intent. Every time AI suggested something, I had to decide whether it fit the system I was building or just looked right in isolation.