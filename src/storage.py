import json
import hashlib
import os

def get_hash(board_name, url, title, date):
    target = f"{board_name}{url}{title}{date}".encode('utf-8')
    return hashlib.md5(target).hexdigest()

def load_seen():
    if os.path.exists('data/seen.json'):
        with open('data/seen.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_seen(seen_list):
    os.makedirs('data', exist_ok=True)
    with open('data/seen.json', 'w', encoding='utf-8') as f:
        json.dump(seen_list[-1000:], f, ensure_ascii=False, indent=2)