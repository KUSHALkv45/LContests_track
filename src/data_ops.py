import pandas as pd
from datetime import date
from src.github_ops import commit_file_to_github

DATA_PATH = "data/events.csv"

def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except:
        return pd.DataFrame(columns=["contest_no", "count", "last_sub_date", "remarks"])

def upsert_event(contest_no, count, remarks):
    df = load_data()
    today = date.today().isoformat()

    if contest_no in df["contest_no"].values:
        df.loc[df["contest_no"] == contest_no, ["count", "last_sub_date", "remarks"]] = [
            count, today, remarks
        ]
    else:
        df = pd.concat([
            df,
            pd.DataFrame([{
                "contest_no": contest_no,
                "count": count,
                "last_sub_date": today,
                "remarks": remarks
            }])
        ], ignore_index=True)

    csv_content = df.to_csv(index=False)
    commit_file_to_github(
        DATA_PATH,
        csv_content,
        f"Update event {contest_no}"
    )

    return df
