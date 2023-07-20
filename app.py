import streamlit as st
import preproesser, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preproesser.pree(data)
    unique_user = df["Name"].unique().tolist()
    unique_user.sort()
    unique_user.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select Unique User", unique_user)

    if st.sidebar.button("Show Analysis"):
        num_message, total_word = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics of Chat")
        colm1,colm2 = st.columns(2)

        with colm1:
            st.header("Total Message")
            st.title(num_message)

        with colm2:
            st.header("Total Words")
            st.title(total_word)
        #Timeline
        st.title("Monthly and daily  timeline")
        colm1, colm2 = st.columns(2)
        with colm1:
            st.header("Monthly Message by Users")
            time = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(time["time"], time["Message"], color = "skyblue")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with colm2:
            st.header("Daily Message by Users")
            daily = helper.daily_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(daily["Everyday"], daily["Message"])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # Dalily user map:
        st.title("Active User Everyday")
        colm1, colm2 = st.columns(2)

        with colm1:
            st.header("Best chatting day")
            busy_day = helper.weekdays(selected_user,df)

            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with colm2:
            st.header("Best chatting Month")
            monthly_busy = helper.montly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(monthly_busy.index, monthly_busy.values, color = "pink")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


        if selected_user=="Overall":
            st.title("Most Busy User")
            x,new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values, color = "skyblue")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        st.title("User Activity In Group Everyday every Hour")

        user_heat = helper.heat_map(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heat)
        st.pyplot(fig)
        #WordCloud
        st.title("World Cloud")
        df_wc = helper.word(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    #Most common word
        st.title("Common Words")
        final = helper.most_common(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(final["Word"],final["Frequency"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

    #Emoji
        st.title("Emoji")
        emoji = helper.emoji_helper(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:

            st.dataframe(emoji)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji[1].head(),labels = emoji[0].head())
            st.pyplot(fig)










