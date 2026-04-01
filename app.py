import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

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
    # Create a fresh Owner and Pet, store them in session_state
    owner = Owner(name=owner_name, available_minutes=available_minutes)
    pet = Pet(name=pet_name, species=species, owner=owner)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.tasks = []  # reset tasks when owner changes
    st.success(f"Saved! {owner_name} with {pet_name} ({species}), {available_minutes} min available.")

# Only show the rest of the app once an owner exists in session_state
if "owner" not in st.session_state:
    st.info("Fill in the owner & pet info above and click Save to get started.")
    st.stop()

owner = st.session_state.owner
pet = owner.get_pets()[0]  # single pet for now

st.divider()

# ── Add Tasks ────────────────────────────────────────────────────────────────

st.subheader(f"Tasks for {pet.name}")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
    pet.add_task(task)
    st.success(f"Added: {task_title}")

current_tasks = pet.get_tasks()
if current_tasks:
    st.table([
        {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────────────

st.subheader("Daily Schedule")

if st.button("Generate schedule"):
    if not current_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        scheduler.build_schedule()
        st.text(scheduler.explain_plan())
