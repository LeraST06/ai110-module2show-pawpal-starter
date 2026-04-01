import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart daily care planning for your pets.")

# ── Owner & Pet setup ────────────────────────────────────────────────────────

st.subheader("Owner & Pet Info")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

available_minutes = st.slider("Minutes available for pet care today", 15, 240, 90, step=5)

if st.button("Save owner & pet"):
    owner = Owner(name=owner_name, available_minutes=available_minutes)
    pet = Pet(name=pet_name, species=species, owner=owner)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Saved! {owner_name} · {pet_name} ({species}) · {available_minutes} min available")

if "owner" not in st.session_state:
    st.info("Fill in the owner & pet info above and click Save to get started.")
    st.stop()

owner: Owner = st.session_state.owner
pet: Pet = owner.get_pets()[0]

st.divider()

# ── Add Tasks ────────────────────────────────────────────────────────────────

st.subheader(f"Tasks for {pet.name}")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    preferred_time = st.text_input("Preferred time (HH:MM, optional)", value="")
with col5:
    frequency = st.selectbox("Repeats", ["none", "daily", "weekly"])

if st.button("Add task"):
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        preferred_time=preferred_time.strip() or None,
        frequency=frequency if frequency != "none" else None,
        due_date=date.today(),
    )
    pet.add_task(task)
    st.success(f"Added: {task_title}")

# Show current task list sorted by time
scheduler = Scheduler(owner=owner)
all_tasks = scheduler.sort_by_time()

if all_tasks:
    st.table([
        {
            "Task": t.title,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Time": t.preferred_time or "—",
            "Repeats": t.frequency or "—",
        }
        for t in all_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────────────

st.subheader("Daily Schedule")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler.build_schedule()

        # Conflict warnings — shown prominently at the top
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ Time conflict: {warning}")

        # Scheduled tasks
        if scheduler.scheduled_tasks:
            st.success(f"Scheduled {len(scheduler.scheduled_tasks)} task(s) — {sum(t.duration_minutes for t in scheduler.scheduled_tasks)} min total")
            st.table([
                {
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Time": t.preferred_time or "—",
                    "Repeats": t.frequency or "—",
                }
                for t in scheduler.scheduled_tasks
            ])
        else:
            st.info("No tasks fit within the available time.")

        # Skipped tasks
        if scheduler.skipped_tasks:
            st.error(f"{len(scheduler.skipped_tasks)} task(s) skipped — not enough time remaining")
            for task in scheduler.skipped_tasks:
                label = f"**{task.title}** ({task.duration_minutes} min, {task.priority} priority)"
                if task.priority == "high":
                    st.error(f"⚠️ {label} — high priority, consider freeing up time!")
                else:
                    st.warning(label)
