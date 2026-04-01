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
- Removed `detect_conflicts()` as a separate method. Conflict detection happens inside `build_schedule()` instead

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- Time budget (`available_minutes`) — tasks that don't fit are skipped entirely
- Priority (high/medium/low) — higher priority tasks are scheduled first
- Preferred time (`HH:MM`) — tasks with a set time are placed before unscheduled ones
- Completion status — already-done tasks are excluded from the daily build

Time budget was the most important constraint because without it, the scheduler has nothing to optimize against. Priority came next since the whole point is making sure the most critical care happens first.

**b. Tradeoffs**

Conflict detection only flags tasks with the **exact same** `preferred_time` string. A 30-minute task at `07:00` and a task at `07:15` won't trigger a warning even though they clearly overlap in real time.

This is reasonable for now because the app doesn't track actual start/end times — it only knows preferred time windows. Adding duration-aware overlap detection would require a proper time arithmetic layer, which is more complexity than the project needs at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
