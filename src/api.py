from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import api_utils as api
import json 
from bson.json_util import dumps

client = MongoClient("mongodb://localhost/analisys")
db = client["analysis"]

app = Flask(__name__)

@app.route('/user/create/<username>')
def create_user(username):
    if api.check_name(db.user, "username", username):
        return "Ya existe ese usuario"
    user = {"username": username}
    user_id = db.user.insert_one(user).inserted_id
    return dumps(str(user_id))


@app.route('/chat/create/<chatname>')
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
def add_user(chat_id):
    user_id = request.args.get("user")
    api.insert_in_collection(db.chat, [chat_id], "users", user_id)
    api.insert_in_collection(db.user, [user_id], "chats", chat_id)
    return dumps(str(chat_id))
    
@app.route('/chat/<chat_id>/list')
def get_messages(chat_id):
    result = []
    messages_ids =  db.chat.find_one({"_id":ObjectId(chat_id)})["messages"]
    for m_id in messages_ids:
        mess = db.message.find_one({"_id":ObjectId(m_id)})
        username = db.user.find_one({"_id": ObjectId(mess["user_id"])})["username"]
        result.append({mess["pos"]: [username, mess["text"]]})
    return dumps(result)


app.run("0.0.0.0", 5000, debug=True)