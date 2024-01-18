#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


import re


# In[3]:


file = open(r"C:\Users\ASUS\Downloads\WhatsApp Chat with 🚕BANGBROS 🚌.txt", 'r', encoding='utf-8')


# In[4]:


data=file.read()


# In[5]:


print(type(data))


# In[6]:


print(data)


# In[7]:


pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'


# In[8]:


messages=re.split(pattern,data)


# In[9]:


messages


# In[10]:


dates=re.findall(pattern,data)


# In[11]:


dates


# In[12]:


len(messages)


# In[13]:


len(dates)


# In[14]:


messages=messages[1:]


# In[15]:


messages


# In[16]:


df=pd.DataFrame({'message':messages,'date':dates})


# In[17]:


df


# In[18]:


df['date']=pd.to_datetime(df['date'],format='%m/%d/%y, %H:%M - ')


# In[19]:


df['dates']=df['date'].dt.date


# In[20]:


df['month']=df['date'].dt.month


# In[21]:


df['year']=df['date'].dt.year


# In[22]:


df['day_of_week']=df['date'].dt.day_of_week


# In[23]:


df['day']=df['date'].dt.day


# In[24]:


df


# In[25]:


df['time']=df['date'].dt.time


# In[26]:


df['hour']=df['date'].dt.hour


# In[27]:


df['minutes']=df['date'].dt.minute


# In[28]:


df['seconds']=df['date'].dt.second


# In[29]:


df['seconds'].nunique()


# In[30]:


df.drop(columns=['seconds','date'],inplace=True)


# In[31]:


df.rename(columns={'dates':'date'})


# In[32]:


df['message'].sample(5).values


# In[33]:


df['message'] = df['message'].apply(lambda x: x.replace('\n', ''))


# In[34]:


df


# In[35]:


df['message'].head(10).values


# In[36]:


df['message'].value_counts()


# In[37]:


users=[]
text=[]
pattern='([\w\W]+?):\s'
for i in df['message']:
    x=re.split(pattern,i)
    if x[1:]:
        users.append(x[1])
        text.append(x[2])
    else:
        users.append('Group Notification')
        text.append(x[0])


# In[38]:


df['user']=users
df['text']=text


# In[39]:


df


# In[40]:


df['user'].value_counts()


# In[41]:


df.drop(columns='message',inplace=True)


# In[42]:


df


# In[43]:


words=[]
for m in df['text']:
    words.extend(m.split(' '))


# In[44]:


len(set(words))


# In[45]:


def fetch_stats(s_user,df):
    if s_user=='Overall':
        num_messages=df.shape[0]
        words = []
        for m in df['text']:
            words.extend(m.split(' '))
        num_words=len(words)
        return num_messages,num_words

    else:
        new_df=df[df['user']==s_user]
        num_messages=new_df.shape[0]
        words = []
        for m in new_df['text']:
            words.extend(m.split(' '))
        num_words=len(words)
        return num_messages,num_words


# In[46]:


n_msgs,n_words=fetch_stats('Overall',df)


# In[47]:


n_msgs


# In[48]:


n_words


# In[49]:


num_media=df[df['text']=='<Media omitted>'].shape[0]


# In[50]:


num_media


# In[51]:


pip install urlextract


# In[52]:


from urlextract import URLExtract


# In[53]:


links=[]
extractor=URLExtract()


# In[54]:


for m in df['text']:
    links.extend(extractor.find_urls(m))


# In[55]:


links


# In[56]:


len(links)


# In[57]:


busiest_users=df.user.value_counts().sort_values(ascending=False).head()


# In[58]:


busiest_users


# In[59]:


n=busiest_users.index
c=busiest_users.values


# In[60]:


n


# In[61]:


c


# In[62]:


ax=sns.barplot(x=n,y=c)
for bars in ax.containers:
    ax.bar_label(bars)


# In[63]:


new_df=round(df.user.value_counts()/df.shape[0]*100,2).sort_values(ascending=False).reset_index().rename(columns={'index':'name','user':'percentage'})


# In[64]:


new_df


# In[65]:


from wordcloud import WordCloud


# In[66]:


wc=WordCloud(height=500,width=500,background_color='white',min_font_size=5)


# In[67]:


wc.generate(df['text'].str.cat(sep=' '))


# In[68]:


plt.imshow(wc)


# In[69]:


abhi=df[df['user']=='Abhi']


# In[70]:


plt.imshow(wc.generate(abhi['text'].str.cat(sep=' ')))


# In[71]:


angad=df[df['user']=='Angad']


# In[72]:


plt.imshow(wc.generate(angad['text'].str.cat(sep=' ')))


# In[73]:


anshul=df[df['user']=='Anshul']


# In[74]:


anshul.shape


# In[75]:


plt.imshow(wc.generate(anshul['text'].str.cat(sep=' ')))


# In[76]:


from collections import Counter


# In[77]:


temp = df[df['user'] != 'Group Notification']
temp = temp[temp['text'] != '<Media omitted>']


# In[78]:


abhi=temp[temp['user']=='Abhi']
plt.imshow(wc.generate(abhi['text'].str.cat(sep=' ')))


# In[79]:


dv=temp[temp['user']=='DV']
plt.imshow(wc.generate(dv['text'].str.cat(sep=' ')))


# In[80]:


from nltk.corpus import stopwords


# In[81]:


s=stopwords.words('english')


# In[82]:


w=[]
for x in temp['text']:
    for word in x.lower().split():
        if word not in s:
            w.append(word)
    


# In[83]:


len(w)


# In[84]:


mcw=pd.DataFrame(Counter(w).most_common(25))


# In[85]:


mcw=mcw.rename(columns={0:'words',1:'values'})


# In[86]:


plt.imshow(wc.generate(mcw['words'].str.cat(sep=' ')))


# In[87]:


mcw


# In[88]:


ravi=temp[temp['user']=='Ravi']


# In[89]:


plt.imshow(wc.generate(ravi['text'].str.cat(sep=' ')))


# In[90]:


import emoji


# In[91]:


ax=sns.barplot(x='words',y='values',data=mcw)
plt.xticks(rotation=90)
for bars in ax.containers:
    ax.bar_label(bars,rotation=90)
plt.title('MOST COMMON WORDS')
plt.show()


# In[92]:


pip install --upgrade emoji


# In[93]:


df


# In[94]:


timeline=df.groupby(['year','month']).count()['text'].reset_index()


# In[95]:


timeline


# In[96]:


timeline['month_name']=timeline['month'].map({1:'January',2:'Febuary',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'})


# In[97]:


timeline


# In[98]:


t=[]
for i in range(timeline.shape[0]):
    t.append(timeline['month_name'][i]+'-'+str(timeline['year'][i]))


# In[99]:


t


# In[100]:


timeline['date']=t


# In[101]:


timeline.drop(columns=['month_name'],inplace=True)


# In[102]:


timeline


# In[103]:


ax=plt.plot(timeline['date'],timeline['text'],'-o')
plt.xticks(rotation=90)
plt.show()


# In[104]:


df


# In[105]:


daily_timeline=df.groupby('dates').count()['text'].reset_index()


# In[106]:


daily_timeline


# In[107]:


plt.figure(figsize=(20,10))
plt.plot(daily_timeline['dates'],daily_timeline['text'],'-v')


# In[108]:


df


# In[109]:


day_line=df.groupby('day_of_week').count()['text'].reset_index()


# In[110]:


day_line


# In[111]:


day_line['day_of_week']=day_line['day_of_week'].map({0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'})


# In[112]:


day_line


# In[113]:


ax=sns.barplot(x='day_of_week',y='text',data=day_line)
for bars in ax.containers:
    ax.bar_label(bars)


# In[114]:


day_line[day_line['text']==day_line['text'].max()]['day_of_week']


# In[115]:


ab=df[df['user']=='Abhi']


# In[116]:


ab


# In[117]:


x=ab.groupby(['dates']).count()['text'].reset_index()


# In[118]:


x


# In[119]:


plt.plot(x['dates'],x['text'])
plt.xticks(rotation=90)


# In[120]:


df


# In[121]:


df['hour'].unique()


# In[122]:


df['period']=df['hour'].apply(lambda x: str(x)+'-'+str(x+1))


# In[123]:


df


# In[124]:


time_ana=df[['period','text','day_of_week']]


# In[125]:


time_ana['day_of_week']=time_ana['day_of_week'].map({0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'})


# In[126]:


time_ana


# In[129]:


tempo=time_ana.groupby('period').count()['text'].reset_index()


# In[132]:


sns.barplot(x='period',y='text',data=tempo)
plt.xticks(rotation='vertical')
plt.show()


# In[133]:


time_ana


# In[140]:


temporary=time_ana.groupby(['period','day_of_week']).count()['text'].reset_index()


# In[142]:


temporary


# In[144]:


sns.heatmap(time_ana.pivot_table(index='day_of_week', columns='period', values='text', aggfunc='count').fillna(0))


# In[145]:


#for one user


# In[146]:


ndf=df[df['user']=='Abhi']


# In[148]:


ndf
ndf=ndf[ndf['text']!='<Media omitted>']


# In[149]:


ndf


# In[151]:


abhi_df=ndf.groupby(['year','month','day_of_week','period']).count()['text'].reset_index()


# In[152]:


abhi_df


# In[157]:


ax=abhi_df.groupby('year').count()['text'].plot(kind='bar')
for bars in ax.containers:
    ax.bar_label(bars)


# In[163]:


sns.heatmap(ndf.groupby(['period','day_of_week']).count()['text'].reset_index().pivot_table(columns='period',values='text',index='day_of_week'))


# In[164]:


ndf


# In[167]:


ndf.groupby('dates').count()['text'].plot(kind='line')
plt.xticks(rotation='vertical')
plt.show()


# In[ ]:




