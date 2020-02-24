import nltk, utils, requests, json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity as distance
from statistics import mean
import pandas as pd
nltk.download('vader_lexicon')



def get_sentiment_analysis_of_chats():
    sia = SentimentIntensityAnalyzer()
    result=dict()
    for chat_id in utils.get_all_ids("chats"):
        messages = json.loads(requests.get(f"{utils.URL}chat/{chat_id}/messages").text)
        pos, neu, neg = ([],[],[])
        for mess in messages:
            pos.append(sia.polarity_scores(list(mess.values())[0][1])["pos"])
            neu.append(sia.polarity_scores(list(mess.values())[0][1])["neu"])
            neg.append(sia.polarity_scores(list(mess.values())[0][1])["neg"])
        result[requests.get(f"{utils.URL}chat/{chat_id}").text] = (mean(pos), mean(neu), mean(neg))
    return sorted(result.items(), key = lambda x: x[1][0], reverse = True)



def get_sentiment_analysis_of_users():
    sia = SentimentIntensityAnalyzer()
    result=dict()
    for user_id in utils.get_all_ids("users"):
        messages = [list(e.values()) for e in json.loads(requests.get(f"{utils.URL}user/{user_id}/messages").text)]
        messages = [k for e in messages for k in e]
        pos, neu, neg = ([],[],[])
        for mess in messages:
            pos.append(sia.polarity_scores(mess)["pos"])
            neu.append(sia.polarity_scores(mess)["neu"])
            neg.append(sia.polarity_scores(mess)["neg"])
        result[requests.get(f"{utils.URL}user/{user_id}").text] = (mean(pos), mean(neu), mean(neg))
    return sorted(result.items(), key = lambda x: x[1][0], reverse = True)

def get_chats_for_user(user_name):
    chats = get_sentiment_analysis_of_chats()
    users = get_sentiment_analysis_of_users()
    user_names = [user[0] for user in users]
    user_values = [user[1] for user in users]
    df_users = pd.DataFrame(user_values, index=user_names, columns=["pos", "neu", "neg"])
    chat_names = [chat[0] for chat in chats]
    chat_values = [chat[1] for chat in chats]
    df_chats = pd.DataFrame(chat_values, index=chat_names, columns=["pos", "neu", "neg"])
    similarity_matrix = distance(df_users, df_chats)
    sim_df = pd.DataFrame(similarity_matrix, columns=df_chats.index, index=df_users.index)
    return sim_df.loc[user_name].head()


#def get_chats_for_user(user_name):
#    chats = get_sentiment_analysis_of_chats()
#    users = get_sentiment_analysis_of_users()
#    user_names = [user[0] for user in users]
#    user_values = [user[1] for user in users]
#    df_users = pd.DataFrame(user_values, index=user_names, columns=["pos", "neu", "neg"])
#    chat_names = [chat[0] for chat in chats]
#    chat_values = [chat[1] for chat in chats]
#    df_chats = pd.DataFrame(chat_values, index=chat_names, columns=["pos", "neu", "neg"])
#    df = df_users.append(df_chats)
#    similarity_matrix = distance(df, df)
#    sim_df = pd.DataFrame(similarity_matrix, columns=df.index, index=df.index)
#    return sim_df.loc[user_name].head()