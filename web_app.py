import os
import uuid
import json
import string
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1 MB in bytes
UPLOAD_FOLDER = './items'
DATA_FOLDER = './data'
PRIVATE_PREFIXES_FILE = './privatePrefixes.txt'
UPLOAD_RECORD_FILE = './upload_record.txt'

# Load private prefixes
private_prefixes = set()
with open(PRIVATE_PREFIXES_FILE, 'r') as f:
    private_prefixes.update(line.strip() for line in f.readlines() if line.strip())

def generate_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def is_valid_code(code):
    return not any(code.startswith(prefix) for prefix in private_prefixes)

def save_upload_record(data):
    with open(UPLOAD_RECORD_FILE, 'a') as f:
        f.write(json.dumps(data) + '\n')

def save_player_data(owner_uuid, data):
    player_file = os.path.join(DATA_FOLDER, f'{owner_uuid}.json')
    player_info = {}
    if os.path.exists(player_file):
        with open(player_file, 'r') as f:
            player_info = json.load(f)
    player_info['custom_code_count'] = player_info.get('custom_code_count', 0) + 1
    player_info['total_code_count'] = player_info.get('total_code_count', 0) + 1
    player_info['total_size'] = player_info.get('total_size', 0) + len(json.dumps(data))
    with open(player_file, 'w') as f:
        json.dump(player_info, f)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        custom_code = data.get('customCode', False)
        owner_uuid = data.get('owner')
        minecraft_id = data.get('minecraftID')
        nbt = data.get('nbt')
        
        if custom_code:
            code = data.get('code')
            if not code:
                return jsonify({'error': 'Custom code is enabled but no code provided'}), 400
            if not is_valid_code(code):
                return jsonify({'error': 'Invalid custom code prefix'}), 400
        else:
            code = generate_random_code()
            while not is_valid_code(code):
                code = generate_random_code()

        expiration = data.get('expiration', '')
        download_limit = data.get('downloadLimit', '')
        visibility = data.get('visibility', '')
        
        upload_info = {
            'customCode': custom_code,
            'owner': owner_uuid,
            'code': code,
            'expiration': expiration,
            'downloadLimit': download_limit,
            'visibility': visibility,
            'minecraftID': minecraft_id,
            'nbt': nbt
        }
        
        # Save upload record
        save_upload_record(upload_info)
        
        # Save player data
        save_player_data(owner_uuid, data)
        
        # Save uploaded file
        file_name = f'{uuid.uuid4()}.json'
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        return jsonify({'success': True, 'message': 'Upload successful', 'code': code}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=25574)
