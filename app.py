import streamlit as st
import helper
from preprocessor import preprocess

# Streamlit app
# Streamlit app
st.set_page_config(layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Please choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)

    # Sidebar - Display options
    st.sidebar.subheader("Options")
    selected_user = st.sidebar.selectbox("Select User", ['OVERALL'] + df['users'].unique().tolist())

    # Main content
    st.title("WhatsApp Chat Analyzer")
    st.markdown("---")

    # Show basic stats
    st.header("Basic Stats")
    num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
    st.write(f"**Total Messages:** {num_messages}")
    st.write(f"**Total Words:** {num_words}")
    st.write(f"**Total Media Shared:** {num_media}")
    st.write(f"**Total Links Shared:** {num_links}")
    st.markdown("---")

    # Expander for detailed analysis
    with st.expander("Detailed Analysis"):
        # Show most busy users
        st.subheader("Most Busy Users")
        helper.most_busy_users(df)
        st.markdown("---")

        # Show user contributions
        st.subheader("User Contributions")
        contributions_df = helper.user_contributions(df)
        st.write(contributions_df)
        st.markdown("---")

        # Show Word Cloud
        st.subheader("Word Cloud")
        wordcloud = helper.generate_wordcloud(selected_user, df)
        st.image(wordcloud.to_array(), use_column_width=True)
        st.markdown("---")

        # Show Most Common Words
        st.subheader("Most Common Words")
        common_words_df = helper.most_common_words(selected_user, df)
        helper.plot_most_common_words(common_words_df)
        st.dataframe(common_words_df)
        st.markdown("---")

        # Show Emoji Analysis
        st.subheader("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user, df)
        st.dataframe(emoji_df)
        st.markdown("---")

        # Show Timeline Analysis
        st.subheader("Message Timeline")
        helper.timeline_analysis(selected_user, df)
        st.markdown("---")

        # Show Daily Activity
        st.subheader("Daily Activity")
        helper.daily_activity_analysis(selected_user, df)
        st.markdown("---")

        # Show Weekly Activity
        st.subheader("Weekly Activity")
        helper.weekly_activity_analysis(selected_user, df)
        st.markdown("---")

        # Show Sentiment Analysis
        st.subheader("Sentiment Analysis")
        helper.sentiment_plot(selected_user, df)
        st.markdown("---")

        # Show Hourly Activity Heatmap
        st.subheader("Hourly Activity Heatmap")
        helper.hourly_activity_heatmap(selected_user, df)
        st.markdown("---")

        # Show Most Active Days and Hours
        st.subheader("Most Active Days and Hours")
        most_active_day, most_active_hour = helper.most_active_days_hours(selected_user, df)
        st.write(f"Most Active Day: {most_active_day}")
        st.write(f"Most Active Hour: {most_active_hour}")

# Check if no file is uploaded
if uploaded_file is None:
    st.info("Please upload a WhatsApp chat file to analyze.")
