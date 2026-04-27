import os

BASE_URL = "https://kcc.go.kr/user.do"
BOARDS = {
    "공지사항": {"pageId": "P02060100", "boardId": "1110"},
    "보도자료": {"pageId": "P02010100", "boardId": "1111"},
    "언론보도대응": {"pageId": "P02010200", "boardId": "1112"},
    "의사일정": {"pageId": "P02020100", "boardId": "1113"},
    "심결정보": {"pageId": "P02030200", "boardId": "1114"},
    "방송정책": {"pageId": "P02040101", "boardId": "1115"},
    "이용자정책": {"pageId": "P02050100", "boardId": "1116"},
    "입법예고": {"pageId": "P05020200", "boardId": "1117"},
    "법령개정": {"pageId": "P05020300", "boardId": "1118"},
    "정책연구": {"pageId": "P02060200", "boardId": "1119"},
    "연차보고서": {"pageId": "P02060300", "boardId": "1120"},
    "기타보고서": {"pageId": "P02060400", "boardId": "1121"},
}

HIGH_PRIORITY_KEYWORDS = ["홈쇼핑", "재승인", "T커머스", "티커머스", "GS샵", "GSSHOP", "GSMYSHOP"]
INCLUDE_KEYWORDS = ["GS리테일", "지에스리테일", "GS홈쇼핑", "지에스홈쇼핑", "심사청문회", "방송채널사용사업자"]
EXCLUDE_KEYWORDS = []

SEND_EMPTY_MAIL = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO")