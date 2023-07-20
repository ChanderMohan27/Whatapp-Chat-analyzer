import re
import pandas as pd
def pree(data):
    pattern = r'\[(.*?)\] (.*?): (.*?)$'
    matches = re.findall(pattern, data, re.MULTILINE)
    df = pd.DataFrame(matches,columns=['Timestamp', 'Name', 'Message'])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format= "%d/%m/%Y, %I:%M:%S %p")
    df["year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month_name()
    df["Month_um"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour
    df["minute"] = df["Timestamp"].dt.minute
    df["Everyday"] = df["Timestamp"].dt.date
    df["day_name"] = df["Timestamp"].dt.day_name()
    period = []
    for hour in df[["day_name", "Hour"]]["Hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))

        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))

        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df["period"] = period

    df.drop("Timestamp", axis=1)

    return df

