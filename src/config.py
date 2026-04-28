import os

# 방통위 공식 RSS 기본 주소
RSS_BASE_URL = "https://kcc.go.kr/user.do"

# 제공해주신 정보를 바탕으로 구성한 전체 게시판 목록
BOARDS = {
    "공지사항": {"pageId": "P02060100", "boardId": "1110", "mode": "list", "view": "rss"},
    "보도자료": {"pageId": "P02010100", "boardId": "1111", "mode": "list", "view": "rss"},
    "언론보도대응": {"pageId": "P02010200", "boardId": "1112", "mode": "list", "view": "rss"},
    "의사일정": {"pageId": "P02020100", "boardId": "1113", "mode": "list", "view": "rss"},
    "심결정보": {"pageId": "P02030200", "boardId": "1114", "mode": "list", "view": "rss"},
    "방송정책": {"pageId": "P02040101", "boardId": "1115", "mode": "list", "view": "rss"},
    "이용자정책": {"pageId": "P02050100", "boardId": "1116", "mode": "list", "view": "rss"},
    "입법예고": {"pageId": "P05020200", "boardId": "1117", "mode": "list", "view": "rss"},
    "법령개정": {"pageId": "P05020300", "boardId": "1118", "mode": "list", "view": "rss"},
    "정책연구": {"pageId": "P02060200", "boardId": "1119", "mode": "list", "view": "rss"},
    "연차보고서": {"pageId": "P02060300", "boardId": "1120", "mode": "list", "view": "rss"},
    "기타보고서": {"pageId": "P02060400", "boardId": "1121", "mode": "list", "view": "rss"},
}

HIGH_PRIORITY_KEYWORDS = ["홈쇼핑", "재승인", "T커머스", "티커머스", "GS샵", "GSSHOP", "GSMYSHOP"]
INCLUDE_KEYWORDS = ["GS리테일", "지에스리테일", "GS홈쇼핑", "지에스홈쇼핑", "심사청문회", "방송채널사용사업자"]
EXCLUDE_KEYWORDS = []

# 테스트를 위해 True로 유지 (신규 자료가 없어도 메일 발송)
SEND_EMPTY_MAIL = True

# 환경변수 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # 깃허브 실행 시 465 또는 587 중 작동하는 것 사용
SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO")