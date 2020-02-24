from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import api_utils as api
import json, sentiment_utils, similarity_utils
from bson.json_util import dumps
from flask_cors import cross_origin

client = MongoClient("mongodb://localhost/analysis")
db = client["analysis"]

app = Flask(__name__)



@app.route('/user/create/<username>')
@cross_origin()
def create_user(username):
    if api.check_name(db.user, "username", username):
        return dumps(str(api.check_name(db.user, "username", username)).strip('"'))
    user = {"username": username}
    user_id = db.user.insert_one(user).inserted_id
    return dumps(str(user_id))


@app.route('/chat/create/<chatname>')
@cross_origin()
def create_chat(chatname):
    users_ids = request.args.get('users').split(",")
    if api.check_name(db.chat, "name", chatname):
        return "Ya existe ese chat"
    chat = {"name": chatname,
            "users": users_ids}
    chat_id = db.chat.insert_one(chat).inserted_id
    api.insert_in_collection(db.user, users_ids, "chats", str(chat_id))
    return dumps(str(chat_id))

@app.route('/chat/<chat_id>/addmessage', methods=['POST'])
@cross_origin()
def add_message(chat_id):
    js = request.get_json()
    messages = list(db.message.find({"chat_id":chat_id}))
    pos = max([mess.get("pos") if mess.get("pos") else 0 for mess in messages]) if len(messages) > 0 else 0
    message = {"text": js["text"],
                "chat_id": chat_id,
                "user_id": js["user"],
                "pos": pos+1}
    message_id = db.message.insert_one(message).inserted_id
    api.insert_in_collection(db.chat, [chat_id] ,"messages", str(message_id))
    return dumps(str(message_id))


@app.route('/chat/<chat_id>/adduser')
@cross_origin()
def add_user(chat_id):
    user_id = request.args.get("user")
    if api.check_user_in_chat(db.chat, chat_id, user_id):
        return "The user is already in the chat"
    api.insert_in_collection(db.chat, [chat_id], "users", user_id)
    api.insert_in_collection(db.user, [user_id], "chats", chat_id)
    return dumps(str(chat_id))
   
# Nueva ruta para devolver los mensajes   
@app.route('/chat/<chat_id>/messages')
@cross_origin()
def get_messages(chat_id):
    result = []
    messages_ids =  db.chat.find_one({"_id":ObjectId(chat_id)})["messages"]
    for m_id in messages_ids:
        mess = db.message.find_one({"_id":ObjectId(m_id)})
        username = db.user.find_one({"_id": ObjectId(mess["user_id"])})["username"]
        result.append({mess["pos"]: [username, mess["text"]]})
    return dumps(result)

# Rutas necesarias para el chat
@app.route('/chat/<user_id>/list')
@cross_origin()
def get_chats(user_id):
    chats_ids =  db.user.find_one({"_id":ObjectId(user_id)})["chats"]
    chats_dicts = {}
    for c_id in list(chats_ids):
        chat_temp = db.chat.find_one({"_id":ObjectId(c_id)})
        chats_dicts[str(chat_temp["_id"])] = chat_temp["name"]
    return dumps(chats_dicts)


@app.route('/user/<user_id>')
@cross_origin()
def get_username(user_id):
    return db.user.find_one({"_id":ObjectId(user_id)})["username"]

@app.route('/username/<username>')
@cross_origin()
def get_user_id(username):
    return str(db.user.find_one({"username":username})["_id"])

@app.route('/chat/<chat_id>')
@cross_origin()
def get_name(chat_id):
    return db.chat.find_one({"_id":ObjectId(chat_id)})["name"]

@app.route('/chats')
def get_all_chats():
    return dumps(db.chat.find({}))

@app.route('/users')
def get_all_users():
    return dumps(db.user.find({}))

@app.route('/user/<user_id>/messages')
def get_all_messages_from_user(user_id):
    return dumps(db.message.find({"user_id":user_id},{"text":1, "_id":0}))

@app.route('/user/<user_name>/chats')
def get_best_chats_for_user(user_name):
    return dumps(sentiment_utils.get_chats_for_user(user_name))

@app.route('/chat/<chat_name>/similarity')
def get_best_chats_for_chat(chat_name):
    return dumps(similarity_utils.get_chat_similarity(chat_name))

@app.route('/user/<user_name>/similarity')
def get_best_users_for_user(user_name):
    return dumps(similarity_utils.get_user_similarity(user_name))

app.run("0.0.0.0", 5000, debug=True)