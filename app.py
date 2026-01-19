import streamlit as st
from src.data_ops import load_data, upsert_event

st.title("📊 Event Tracker")

df = load_data()

# ---------- VIEW ----------
st.header("View Completed Events")

show_events = st.checkbox("Show completed events")

if show_events and not df.empty:

    # ---- SEARCH ----
    search_id = st.number_input(
        "Search by Contest No (leave 0 to disable)",
        min_value=0,
        step=1
    )

    filtered_df = df

    if search_id != 0:
        filtered_df = df[df["contest_no"] == search_id]

        if filtered_df.empty:
            st.info("No event found for this Contest No.")

    if not filtered_df.empty:
        st.caption("💡 Tip: Click on column headers to sort")
        st.dataframe(filtered_df, use_container_width=True)

elif show_events:
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
