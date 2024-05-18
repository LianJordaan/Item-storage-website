import os
import uuid
from flask import Flask, request

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # 1 MB in bytes

UPLOAD_RECORD_FILE = './upload_record.txt'

@app.route('/', methods=['GET'])
def example():
    try:
        return "Hello World!"
    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=25574)
