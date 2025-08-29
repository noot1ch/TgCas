import json

with open('database/database.json', 'r') as file:
    db = json.load(file)

def save_db(db):
    with open('database/database.json', 'w', encoding='UTF-8') as file:
        json.dump(db, file, indent=2)