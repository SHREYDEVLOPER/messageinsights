import pandas as pd
import re

# Define the preprocess function
def preprocess(data):
    # Define the pattern to extract messages and dates
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s)'

    # Extract messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Ensure messages are aligned correctly by skipping the initial empty string
    messages = [messages[i] for i in range(1, len(messages), 2)]

    # Ensure both lists are of the same length
    if len(messages) != len(dates):
        print("Error: Messages and dates lists are not of the same length.")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean and convert 'message_date' to datetime
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ').str.strip()
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p -')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add date-related columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
