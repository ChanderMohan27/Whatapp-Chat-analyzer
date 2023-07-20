from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
def fetch_stats(selected_user,df):
    if selected_user == "Overall":
        total_message = df.shape[0]
        words = []
        for message in df["Message"]:
            words.extend(message.split())
        return total_message, len(words)
    else:
        new_df = df[df["Name"]==selected_user]
        total_message = new_df.shape[0]
        words = []
        for message in new_df["Message"]:
            words.extend(message.split())
        return total_message, len(words)
def most_busy_user(df):
    x = df["Name"].value_counts().head()
    new_df = round((df["Name"].value_counts()/df.shape[0])*100,2).reset_index().rename\
        (columns = {"Name":"User","count":"Percentage"})
    return x, new_df
def word(selected_user,df):
    if selected_user == "Overall":
        wc = WordCloud(width=500,height=500, min_font_size=10,background_color="white")
        df_wc = wc.generate(df["Message"].str.cat(sep = " "))

        return df_wc
    else:
        new_df = df[df["Name"] == selected_user]
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
        df_wc = wc.generate(new_df["Message"].str.cat(sep=" "))
        return df_wc

def most_common(selected_user,df):
    f = open("stop_word.txt","r")
    stop_words = f.read()
    words = []
    fit_df = df[df["Name"] != "group_notification"]
    fit_df = df[df["Message"] != "<Media omitted>\n"]
    if selected_user == "Overall":
        for message in fit_df["Message"]:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)


    else:
        new_df = fit_df[fit_df["Name"] == selected_user]

        for message in new_df["Message"]:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
    final = pd.DataFrame(Counter(words).most_common(20))
    final = final.rename(columns = {0:"Word", 1:"Frequency"})
    return final

def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]

    emojis = []
    for message in df["Message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]

    time = df.groupby(["year", "Month_um", "Month"]).count()["Message"].reset_index()
    timef = []
    for i in range(time.shape[0]):
        timef.append(((time["Month"][i]) + "-" + str(time["year"][i])))
    time["time"] = timef
    return time

def daily_timeline(selected_user, df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]
    daily_timeline = df.groupby("Everyday").count()["Message"].reset_index()
    return daily_timeline

def weekdays(selected_user,df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]

    return df["day_name"].value_counts()

def montly_activity(selected_user,df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]
    return df["Month"].value_counts()

def heat_map(selected_user,df):
    if selected_user!="Overall":
        df = df[df["Name"]==selected_user]

    activity_heat_map = df.pivot_table(index = "day_name", columns = "period", values = "Message", aggfunc = "count"). fillna(0)

    return activity_heat_map
