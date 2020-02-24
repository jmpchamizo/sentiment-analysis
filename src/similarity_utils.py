import json, requests, utils
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np


def get_users_dataframe_words():
    result = pd.DataFrame()
    for chat_id in utils.get_all_ids("chats"):
        messages = requests.get(f"{utils.URL}chat/{chat_id}/messages")
        messages_tuple = [(list(mess.values())[0][0],list(mess.values())[0][1]) for mess in json.loads(messages.text)]
        messages_text = [mess[1] for mess in messages_tuple]
        messages_person = [mess[0] for mess in messages_tuple]
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(messages_text)
        messages_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(messages_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=messages_person)
        result = result.append(df, sort=True).fillna(0)
    return result.groupby(result.index).sum()

def get_user_similarity(user_name):
    try:
        sim_df = get_dataframe_similarity_users()
        return sim_df[user_name].sort_values(ascending=False).head()
    except KeyError:
        return "User doesn't exist"
    

def get_dataframe_similarity_users():
    df = get_users_dataframe_words()
    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=df.index, index=df.index)
    np.fill_diagonal(sim_df.values, 0)
    return sim_df


# Mismos calculos para los chats:

def get_chats_dataframe_words():
    result = pd.DataFrame()
    for chat_id in utils.get_all_ids("chats"):
        messages = requests.get(f"{utils.URL}chat/{chat_id}/messages")
        chat_name = requests.get(f"{utils.URL}chat/{chat_id}")
        messages_tuple = [(chat_name.text,list(mess.values())[0][1]) for mess in json.loads(messages.text)]
        messages_text = [mess[1] for mess in messages_tuple]
        messages_chat = [mess[0] for mess in messages_tuple]
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(messages_text)
        messages_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(messages_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=messages_chat)
        result = result.append(df, sort=True).fillna(0)
    return result.groupby(result.index).sum()



def get_dataframe_similarity_chats():
    df = get_chats_dataframe_words()
    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=df.index, index=df.index)
    np.fill_diagonal(sim_df.values, 0)
    return sim_df

def get_chat_similarity(chat_name):
    try:
        sim_df = get_dataframe_similarity_chats()
        return sim_df[chat_name].sort_values(ascending=False).head()
    except KeyError:
        return "Chat doesn't exist"