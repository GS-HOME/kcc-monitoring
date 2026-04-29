import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import *

def send_mail(items, date_str):
    if not items and not SEND_EMPTY_MAIL: return
    count = len(items)
    # KCC를 KMCC로 변경
    subject = f"[방미통위(KMCC) 모니터링] {date_str} 신규 자료 {count}건"
    
    html = f"<h2>{date_str} KMCC 모니터링 결과 (총 {count}건)</h2>"
    # ... (이하 동일)