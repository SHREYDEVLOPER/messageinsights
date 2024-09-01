import re
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
from collections import Counter
import emoji
from textblob import TextBlob
import seaborn as sns

# Ensure consistent style for plots
sns.set_style("whitegrid")

def fetch_stats(selected_user, df):
    if selected_user == 'OVERALL':
        num_messages = df.shape[0]
        num_words = df['message'].apply(lambda x: len(x.split())).sum()
        num_media_messages = df[df['message'].str.contains('<Media omitted>|<image omitted>|<video omitted>', na=False)].shape[0]
        num_links = df['message'].apply(lambda x: bool(re.search(r'http[s]?://', x))).sum()
    else:
        user_df = df[df['users'] == selected_user]
        num_messages = user_df.shape[0]
        num_words = user_df['message'].apply(lambda x: len(x.split())).sum()
        num_media_messages = user_df[user_df['message'].str.contains('<Media omitted>|<image omitted>|<video omitted>', na=False)].shape[0]
        num_links = user_df['message'].apply(lambda x: bool(re.search(r'http[s]?://', x))).sum()

    return num_messages, num_words, num_media_messages, num_links

def most_busy_users(df):
    user_counts = df['users'].value_counts().head()
    names = user_counts.index
    counts = user_counts.values
    plt.figure(figsize=(10, 5))
    sns.barplot(x=names, y=counts, palette='viridis')
    plt.xlabel('Users')
    plt.ylabel('Message Count')
    plt.xticks(rotation='vertical')
    plt.title('Most Busy Users')
    st.pyplot(plt)

def user_contributions(df):
    user_counts = df['users'].value_counts()
    total_messages = df.shape[0]
    contributions = (user_counts / total_messages) * 100
    contributions_df = contributions.reset_index()
    contributions_df.columns = ['User', 'Contribution (%)']
    return contributions_df

def generate_wordcloud(selected_user, df):
    if selected_user == 'OVERALL':
        text = ' '.join(df['message'])
    else:
        user_df = df[df['users'] == selected_user]
        text = ' '.join(user_df['message'])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def most_common_words(selected_user, df, n=20):
    if selected_user == 'OVERALL':
        messages = df['message']
    else:
        messages = df[df['users'] == selected_user]['message']

    all_words = ' '.join(messages).split()
    word_counts = Counter(all_words)
    common_words_df = pd.DataFrame(word_counts.most_common(n), columns=['Word', 'Frequency'])
    return common_words_df

def emoji_analysis(selected_user, df):
    if selected_user == 'OVERALL':
        messages = df['message']
    else:
        messages = df[df['users'] == selected_user]['message']

    emojis = [char for message in messages for char in message if char in emoji.EMOJI_DATA]
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Frequency'])
    return emoji_df

def plot_most_common_words(common_words_df):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Word', y='Frequency', data=common_words_df, palette='magma')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation='vertical')
    plt.title('Most Common Words')
    st.pyplot(plt)

def timeline_analysis(selected_user, df):
    if selected_user == 'OVERALL':
        timeline_df = df.groupby(df['date'].dt.date).size().reset_index(name='message_count')
    else:
        user_df = df[df['users'] == selected_user]
        timeline_df = user_df.groupby(user_df['date'].dt.date).size().reset_index(name='message_count')
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='date', y='message_count', data=timeline_df, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Message Count')
    plt.title(f'Message Timeline for {selected_user}')
    plt.xticks(rotation='vertical')
    st.pyplot(plt)

def daily_activity_analysis(selected_user, df):
    if selected_user == 'OVERALL':
        daily_df = df.groupby(df['date'].dt.hour).size().reset_index(name='message_count')
    else:
        user_df = df[df['users'] == selected_user]
        daily_df = user_df.groupby(user_df['date'].dt.hour).size().reset_index(name='message_count')

    plt.figure(figsize=(10, 5))
    sns.lineplot(x='date', y='message_count', data=daily_df, marker='o')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Message Count')
    plt.title(f'Daily Activity Timeline for {selected_user}')
    plt.xticks(range(24))
    st.pyplot(plt)

def weekly_activity_analysis(selected_user, df):
    if selected_user == 'OVERALL':
        weekly_df = df.groupby(df['date'].dt.dayofweek).size().reset_index(name='message_count')
    else:
        user_df = df[df['users'] == selected_user]
        weekly_df = user_df.groupby(user_df['date'].dt.dayofweek).size().reset_index(name='message_count')

    weekly_df['date'] = weekly_df['date'].apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x])

    plt.figure(figsize=(10, 5))
    sns.lineplot(x='date', y='message_count', data=weekly_df, marker='o')
    plt.xlabel('Day of the Week')
    plt.ylabel('Message Count')
    plt.title(f'Weekly Activity Timeline for {selected_user}')
    st.pyplot(plt)

def sentiment_analysis(selected_user, df):
    if selected_user == 'OVERALL':
        df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    else:
        user_df = df[df['users'] == selected_user]
        user_df['sentiment'] = user_df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)

    sentiment_df = df if selected_user == 'OVERALL' else user_df
    return sentiment_df

def sentiment_plot(selected_user, df):
    sentiment_df = sentiment_analysis(selected_user, df)
    plt.figure(figsize=(10, 5))
    sns.histplot(sentiment_df['sentiment'], bins=20, kde=True, color='blue')
    plt.xlabel('Sentiment')
    plt.ylabel('Message Count')
    plt.title(f'Sentiment Analysis for {selected_user}')
    st.pyplot(plt)

def hourly_activity_heatmap(selected_user, df):
    if selected_user == 'OVERALL':
        df['hour'] = df['date'].dt.hour
        df['day'] = df['date'].dt.day_name()
    else:
        user_df = df[df['users'] == selected_user]
        user_df['hour'] = user_df['date'].dt.hour
        user_df['day'] = user_df['date'].dt.day_name()

    activity_df = df if selected_user == 'OVERALL' else user_df
    heatmap_data = activity_df.pivot_table(index='day', columns='hour', values='message', aggfunc='count').fillna(0)
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu')
    plt.title(f'Hourly Activity Heatmap for {selected_user}')
    st.pyplot(plt)

def most_active_days_hours(selected_user, df):
    if selected_user == 'OVERALL':
        df['hour'] = df['date'].dt.hour
        df['day'] = df['date'].dt.day_name()
    else:
        user_df = df[df['users'] == selected_user]
        user_df['hour'] = user_df['date'].dt.hour
        user_df['day'] = user_df['date'].dt.day_name()

    activity_df = df if selected_user == 'OVERALL' else user_df
    most_active_day = activity_df['day'].mode()[0]
    most_active_hour = activity_df['hour'].mode()[0]

    return most_active_day, most_active_hour
