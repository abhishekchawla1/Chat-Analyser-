import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    messages = messages[1:]
    df = pd.DataFrame({'message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M - ')
    df['dates'] = df['date'].dt.date
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.day_of_week
    df['day'] = df['date'].dt.day
    df['time'] = df['date'].dt.time
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['seconds'] = df['date'].dt.second
    df.drop(columns=['seconds', 'date'], inplace=True)
    df.rename(columns={'dates': 'date'})
    df['message'] = df['message'].apply(lambda x: x.replace('\n', ''))
    users = []
    text = []
    pattern = '([\w\W]+?):\s'
    for i in df['message']:
        x = re.split(pattern, i)
        if x[1:]:
            users.append(x[1])
            text.append(x[2])
        else:
            users.append('Group Notification')
            text.append(x[0])
    df['user'] = users
    df['text'] = text
    df.drop(columns='message', inplace=True)
    return df