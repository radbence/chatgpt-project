from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# A JSON fájl neve és elérési útja
json_file_path = 'conversations.json'

# Ellenőrizzük, hogy a fájl létezik-e, ha nem, létrehozzuk
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump({}, file)

@app.route('/username', methods=['GET'])
def get_username():
    # Lekérjük a felhasználó nevét (pl. authentikációból vagy más forrásból)
    username = request.args.get('username', None)
    if username:
        return jsonify({"username": username}), 200
    else:
        return jsonify({"error": "Username not provided"}), 400

@app.route('/save', methods=['POST'])
def save_conversation():
    data = request.get_json()
    username = data.get('username')
    content = data.get('content')
    
    if not username or not content:
        return jsonify({"error": "Invalid input"}), 400
    
    with open(json_file_path, 'r+') as file:
        conversations = json.load(file)
        if username not in conversations:
            conversations[username] = []
        conversations[username].append({'content': content})
        file.seek(0)
        json.dump(conversations, file, indent=4)
    
    return jsonify({"message": "Conversation saved!"}), 201

@app.route('/load', methods=['GET'])
def load_conversations():
    username = request.args.get('username', None)
    
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    with open(json_file_path, 'r') as file:
        conversations = json.load(file)
        user_conversations = conversations.get(username, [])
    
    return jsonify(user_conversations), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
