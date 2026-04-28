import hashlib
import os

DB_FILE = "seen_posts.txt"

def get_hash(board_name, url, title, extra=""):
    base_str = f"{board_name}_{url}_{title}_{extra}"
    return hashlib.md5(base_str.encode('utf-8')).hexdigest()

def load_seen():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_seen(hashes):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        unique_hashes = list(dict.fromkeys(hashes))
        f.write("\n".join(unique_hashes[-1000:]))