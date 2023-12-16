#! /usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ICloud:
    def __init__(self):
        self.server = smtplib.SMTP('smtp.mail.me.com', 587)
        # print(self.server.ehlo())
        # Start the TLS connection
        self.server.starttls()

    # def close(self):
    #     self.server.quit()

    def login(self) -> str:
        # app-specific password generated on https://appleid.apple.com/account/manage
        with open('auth/icloud.txt', 'r') as file:
            sender = file.readline().strip()
            password = file.readline().strip()
        self.server.login(sender, password)
        return sender

    def send(self, sender, recipient, subject, body):
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        self.server.sendmail(sender, recipient, message.as_string())


def main():
    ic = ICloud()
    sender = ic.login()
    ic.send(sender, sender, "Hi, 11235", "test from Python")


if __name__ == "__main__":
    main()
