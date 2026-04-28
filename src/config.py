import os

# 방송통신위원회 기본 도메인
RSS_BASE_URL = "https://www.kmcc.go.kr"

# 사용자 제공 게시판 직접 접근 URL 설정
BOARDS = {
    "공지사항": {"url": "https://www.kmcc.go.kr/user.do?page=A05020000&dc=K05020000&boardId=1112"},
    "보도자료": {"url": "https://www.kmcc.go.kr/user.do?page=A05030000&dc=K05030000&boardId=1113"},
    "언론보도대응": {"url": "https://www.kmcc.go.kr/user.do?page=A05030500&dc=K05035500&boardId=1171"},
    "의사일정": {"url": "https://www.kmcc.go.kr/user.do?page=A02010100&dc=K02010100&boardId=1003"},
    "심결정보": {"url": "https://www.kmcc.go.kr/user.do?page=A02010800&dc=K02010800&boardId=1119"},
    "방송정책": {"url": "https://www.kmcc.go.kr/user.do?page=A02020400&dc=K02020400&boardId=1006"},
    "이용자정책": {"url": "https://www.kmcc.go.kr/user.do?page=A02020600&dc=K02020600&boardId=1008"},
    "입법예고": {"url": "https://www.kmcc.go.kr/user.do?page=A02030900&dc=K02030900&boardId=1101"},
    "법령개정": {"url": "https://www.kmcc.go.kr/user.do?page=A02031000&dc=K02031000"},
    "정책연구": {"url": "https://www.kmcc.go.kr/user.do?page=A02160300&dc=K02160300&boardId=1022"},
    "연차보고서": {"url": "https://www.kmcc.go.kr/user.do?page=A02050300&dc=K02050300&boardId=1078"},
    "기타보고서": {"url": "https://www.kmcc.go.kr/user.do?page=A02050200&dc=K02050200&boardId=1025"},
}

# 키워드 설정
HIGH_PRIORITY_KEYWORDS = ["홈쇼핑", "재승인", "T커머스", "티커머스", "GS샵", "GSSHOP", "GSMYSHOP"]
INCLUDE_KEYWORDS = ["GS리테일", "지에스리테일", "GS홈쇼핑", "지에스홈쇼핑", "심사청문회", "방송채널사용사업자"]
EXCLUDE_KEYWORDS = []

# 메일 발송 관련 설정
SEND_EMPTY_MAIL = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 깃허브 액션 Secrets에서 환경 변수를 읽어옴
SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO")