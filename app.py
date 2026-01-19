import streamlit as st
from src.data_ops import load_data, upsert_event

st.title("📊 Event Tracker")

# ---------- VIEW ----------
st.header("View Completed Events")

df = load_data()

sort_col = st.selectbox(
    "Sort by column",
    options=["contest_no", "count", "last_sub_date"]
)

sort_order = st.radio(
    "Sort order",
    options=["Ascending", "Descending"],
    horizontal=True
)

ascending = sort_order == "Ascending"

if not df.empty:
    st.dataframe(
        df.sort_values(by=sort_col, ascending=ascending),
        use_container_width=True
    )
else:
    st.info("No events yet.")

# ---------- ADD / UPDATE ----------
st.header("Add / Update Event")

with st.form("add_event"):
    contest_no = st.number_input("Contest No", min_value=1, step=1)
    count = st.number_input("Count", min_value=0, step=1)
    remarks = st.text_input("Remarks")
    submitted = st.form_submit_button("Save")

if submitted:
    upsert_event(int(contest_no), int(count), remarks)
    st.success("Committed to GitHub successfully ✅")
    st.experimental_rerun()
