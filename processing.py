from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import emoji
import pandas as pd

def fetch_stats(s_user,df):
    extractor=URLExtract()
    if s_user=='Overall':
        links = []
        num_messages=df.shape[0]
        words = []
        for m in df['text']:
            words.extend(m.split(' '))
        num_words=len(words)
        num_media=df[df['text']=='<Media omitted>'].shape[0]
        for m in df['text']:
            links.extend(extractor.find_urls(m))
        num_links=len(links)
        return num_messages,num_words, num_media,num_links

    else:
        new_df=df[df['user']==s_user]
        num_messages=new_df.shape[0]
        words = []
        for m in new_df['text']:
            words.extend(m.split(' '))
        num_media=new_df[new_df['text']=='<Media omitted>'].shape[0]
        for m in df['text']:
            links.extend(extractor.find_urls(m))
        num_links=len(links)
        return num_messages,num_words, num_media, num_links


def fetch_busy(df):
    b_user=df.user.value_counts().sort_values(ascending=False).head()
    new_df=round(df.user.value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return b_user,new_df

def create_wc(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_user]
    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['text'] != '<Media omitted>']
    wc=WordCloud(width=500,height=500,min_font_size=5,background_color='white')
    w=wc.generate(temp['text'].str.cat(sep=' '))
    return w

def fetch_most_common(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_user]
    s=stopwords.words('english')
    w=[]
    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['text'] != '<Media omitted>']
    for i in temp:
        for words in i.lower().split():
            if words not in s:
                w.append(words)
    mc=pd.DataFrame(Counter(words).most_common(25))
    mc=mc.rename(columns={0:'name',1:'values'})

    wc=WordCloud(height=500,width=500,min_font_size=5,background_color='white')
    w=wc.generate(mc['name'].str.cat(sep=' '))
    return mc,w

def emoji_analyse(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_user]
    em=[]
    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['text'] != '<Media omitted>']
    for i in temp['text']:
        em.extend([x for x in i if x in emoji.UNICODE_EMOJI['en']])
        edf=pd.DataFrame(Counter(em).most_common(len(Counter(em))))
        edf=edf.rename({0:'emoji',1:'values'})
        return edf

def timeanalysis(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_user]
    timeline=df.groupby(['year','month']).count()['text'].reset_index()
    timeline['month_name'] = timeline['month'].map(
        {1: 'January', 2: 'Febuary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
         9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    t = []
    for i in range(timeline.shape[0]):
        t.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))
    timeline['date']=ttimeline.drop(columns=['month_name'],inplace=True)
    return timeline

def dailyanalysis(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_name]
    daily_timeline = df.groupby('dates').count()['text'].reset_index()
    return daily_timeline

def time_ana(s_user,df):
    if s_user!='Overall':
        df=df[df['user']==s_user]
    time_ana = df[['period', 'text', 'day_of_week']]
    time_ana['day_of_week'] = time_ana['day_of_week'].map(
        {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
    temporary = time_ana.groupby(['period', 'day_of_week']).count()['text'].reset_index()
    return sns.heatmap(time_ana.pivot_table(index='day_of_week', columns='period', values='text', aggfunc='count').fillna(0))
