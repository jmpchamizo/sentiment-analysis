from bson.objectid import ObjectId

def insert_in_collection(bbdd, items_ids, field, new_item_id):
     for item_id in items_ids:
        item = bbdd.find_one({"_id": ObjectId(item_id)})
        item_field = item[field] if item.get(field) else []
        item_field.append(new_item_id)
        query = { "_id": item.get("_id") }
        newvalues = { "$set": { field: item_field } }
        bbdd.update_one(query, newvalues)

def check_name(bbdd, field, name):
    item = bbdd.find_one({field: name})
    return item["_id"] if item else None


def check_user_in_chat(bbdd, chat_id, user_id):
    item = bbdd.find_one({"_id": ObjectId(chat_id)})
    return user_id in item["users"]