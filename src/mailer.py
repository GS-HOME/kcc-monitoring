import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import *

def send_mail(items, date_str):
    if not items and not SEND_EMPTY_MAIL:
        print("발송할 항목이 없고 빈 메일 설정이 비활성화되어 있습니다.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = MAIL_TO
        count = len(items)
        msg['Subject'] = f"[방미통위(KMCC) 모니터링] {date_str} 신규 자료 {count}건"

        html = f"<h2>{date_str} KMCC 모니터링 결과 (총 {count}건)</h2>"
        for item in items:
            html += f"""
            <div style="margin-bottom: 20px; padding: 10px; border: 1px solid #ddd;">
                <h3>[{item['board_name']}] {item['title']}</h3>
                <p><strong>등록일:</strong> {item.get('date', 'N/A')}</p>
                <p><strong>요약:</strong> {item.get('summary', '요약 정보 없음')}</p>
                <p><a href="{item['url']}">원문 바로가기</a></p>
            </div>
            """
        
        msg.attach(MIMEText(html, 'html'))

        # SMTP 연결 및 발송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            if not SMTP_USER or not SMTP_APP_PASSWORD:
                raise ValueError("SMTP 계정 정보가 설정되지 않았습니다 (Secrets 확인 필요)")
            
            server.login(SMTP_USER, SMTP_APP_PASSWORD)
            server.send_message(msg)
            
        print(f"메일 발송 성공! (수신: {MAIL_TO})")

    except Exception as e:
        print(f"!!! 메일 발송 에러 발생: {e}")
        # 깃허브 액션에서 에러를 인지할 수 있도록 예외를 다시 발생시킴
        raise e