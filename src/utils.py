import requests,json

URL = "http://localhost:5000/"

def get_all_ids(document):
    document = requests.get(f"{URL}{document}")
    return [list(chat["_id"].values())[0] for chat in json.loads(document.text)]