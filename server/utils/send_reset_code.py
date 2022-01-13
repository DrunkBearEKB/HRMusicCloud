import sys
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


EMAIL = 'HRMusicCloud@gmail.com'
SUBJECT = 'Reset your HRMusicCloud password!'


def send_reset_email(email_to: str, address: str, reset_code: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = email_to
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(
        f'<html>'
        f'<head></head>'
        f'<body>'
        '<div>'
        f'<h2>Reset your HRMusicCloud password!</h2>'
        f'<p>Use this link to reset your password:'
        f'<p>{address}login/reset-password/{reset_code}</p>'
        f'<p>For your security, this link will expire in 48 hours.</p>'
        f'<p>If you didn\'t request this change, please don\'t use '
        f'this link!</p>'
        f'</div>'
        f'</body>'
        f'</html>',
        'html'
    ))

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(
        user=EMAIL,
        password='18723654'  # знаю, что так пароль хранить не надо,
        # но тут это не критично, т.к. это ненужный аккаунт
    )
    smtp_server.sendmail('HRMusicCloud@gmail.com', email_to, msg.as_string())
    smtp_server.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--to')
    parser.add_argument('--address')
    parser.add_argument('--code')
    args = parser.parse_args()

    send_reset_email(args.to, args.address, args.code)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
