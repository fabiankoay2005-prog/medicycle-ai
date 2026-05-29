import pandas as pd
import os

FILE = "festival_calendar.csv"

def load_festivals():

    if not os.path.exists(FILE):
        return pd.DataFrame(
            columns=[
                "festival",
                "start_date",
                "end_date",
                "crowd_size",
                "risk_level"
            ]
        )

    return pd.read_csv(FILE)

def add_festival(
        festival,
        start_date,
        end_date,
        crowd_size,
        risk_level):

    df = load_festivals()

    new_row = {
        "festival": festival,
        "start_date": start_date,
        "end_date": end_date,
        "crowd_size": crowd_size,
        "risk_level": risk_level
    }

    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df.to_csv(FILE,index=False)

def get_upcoming_festival():

    df = load_festivals()

    if len(df)==0:
        return None

    df["start_date"] = pd.to_datetime(df["start_date"])

    today = pd.Timestamp.today()

    future = df[df["start_date"]>=today]

    if len(future)==0:
        return None

    return future.sort_values("start_date").iloc[0]