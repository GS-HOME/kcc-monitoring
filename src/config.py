import os

# 방통위 공식 RSS 기본 주소
RSS_BASE_URL = "https://kcc.go.kr/user.do"

# RSS 제공 보드 ID 리스트
BOARDS = {
    "공지사항": {"pageId": "P02060100", "boardId": "1110", "mode": "list", "view": "rss"},
    "보도자료": {"pageId": "P02010100", "boardId": "1111", "mode": "list", "view": "rss"},
    "해명자료": {"pageId": "P02010200", "boardId": "1112", "mode": "list", "view": "rss"},
}

HIGH_PRIORITY_KEYWORDS = ["홈쇼핑", "재승인", "T커머스", "티커머스", "GS샵", "GSSHOP", "GSMYSHOP"]
INCLUDE_KEYWORDS = ["GS리테일", "지에스리테일", "GS홈쇼핑", "지에스홈쇼핑", "심사청문회", "방송채널사용사업자"]
EXCLUDE_KEYWORDS = []

SEND_EMPTY_MAIL = True # 테스트 완료 후 False로 변경 권장
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO")