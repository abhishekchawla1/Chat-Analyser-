import streamlit as st
import Preprocess,processing
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.sidebar.title('WhatsApp Chat Analyser')
up_file=st.sidebar.file_uploader("Choose a File")
if up_file is not None:
    bytes_d=up_file.getvalue()
    data=bytes_d.decode("utf-8")
    df=Preprocess.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    s_user=st.sidebar.selectbox("Show analysis with respect to", user_list)
    if st.sidebar.button('Show Analysis'):
        n_msgs,n_words,n_media,n_links=processing.fetch_stats(s_user,df)

        st.title('Top Statistics')

        c1,c2,c3,c4=st.columns(4)
        with c1:
            st.header('Total Messages')
            st.title(n_msgs)
        with c2:
            st.header('Total Words')
            st.title(n_words)
        with c3:
            st.header('Total Media')
            st.title(n_media)
        with c4:
            st.header('Total Links')
            st.title(n_links)

        #Busiest users in groups

        if s_user=='Overall':
            st.title('Busiest Users')
            b_u,ndf = processing.fetch_busy(df)
            n=b_u.index
            c=b_u.values
            fig,ax=plt.subplots()
            c1,c2=st.columns(2)
            with c1:
                ax.bar(n,c)
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with c2:
                st.dataframe(ndf)

        #WordCloud

        plt.title('WordCloud')
        cld=processing.create_wc(s_user,df)
        fig,ax=plt.subplots()
        ax.imshow(cld)
        st.pyplot(fig)

        #particular top 25

        plt.title('Most_common_Words')
        mcw,cd=processing.fetch_most_common(s_user,df)
        st.dataframe(mcw)
        fi,ax=plt.subplots()
        ax.imshow(cd)
        st.pyplot(fi)

        #emoji detection

        st.title('EMOJI ANALYSIS')
        emo_df=processing.emoji_analyse(s_user,df)
        c1,c2=st.columns(2)
        with c1:
            st.dataframe(emo_df)
        with c2:
            f,a=plt.subplots()
            a.pie(emo_df[1].head(),labels=emo_df[0].head(),autopct='%0.2f')
            st.pyplot(f)

        #time based analysis

        st.title('Monthly Timeline')
        t=processing.timeanalysis(s_user,df)
        figure,axis=plt.subplots()
        axis.plot(t['date'],t['text'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title('Daily Timeline')
        p=processing.dailyanalysis(s_user,df)
        fig,ax=plt.subplots()
        plt.figure(figsize=(20, 10))
        ax.plot(p['dates'], p['text'], '-v')
        st.pyplot(fig)

        #activity
        st.title('Week Day Analysis')
        day_line = df.groupby('day_of_week').count()['text'].reset_index()
        day_line['day_of_week'] = day_line['day_of_week'].map(
            {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
        fig,ax = sns.barplot(x='day_of_week', y='text', data=day_line)
        for bars in ax.containers:
            ax.bar_label(bars)
        st.pyplot(fig)
        st.title('Most Busy Day')
        p=day_line[day_line['text']==day_line['text'].max()]['day_of_week']
        st.title(p)

        #time analysis week wise

        st.title('Heatmap for Daily Analysis')
        fig,ax=plt.subplots()
        ax=processing.time_ana(s_user,df)
        st.pyplot(fig)



























