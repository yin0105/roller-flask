from threading import Thread
from flask import flash, render_template, current_app
from flask_mail import Message

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app import mail


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('info@whosedoctor.com', 'urtcnsqexmoqjnwj')

def send_test_mail(body):
    sender_email = current_app.config['ADMINS'][0]
    receiver_email = 'info@whosedoctor.com'

    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    filename = "example.txt"
    msg.attach(MIMEText(open(filename).read()))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj: 
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('info@whosedoctor.com', 'urtcnsqexmoqjnwj')
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)


def send_email_verification(user):
    token = user.get_email_token()
    send_email('Confirm Your Email Address', 
                sender=current_app.config['ADMINS'][0], 
                recipients=[user.email], 
                text_body=render_template('email/verify_email.txt', 
                                            user=user, 
                                            token=token), 
                html_body=render_template('email/verify_email.html', 
                                            user=user, 
                                            token=token))

# newsletter
def send_email_newsletter_verification(user):
    token = user.get_email_token()
    send_email('Lucky Winners!', 
                sender=current_app.config['ADMINS'][0], 
                recipients=[user.email], 
                text_body=render_template('email/verify_newsletter_email.txt', 
                                            user=user, 
                                            token=token), 
                html_body=render_template('email/verify_newsletter_email.html', 
                                            user=user, 
                                            token=token))


# doctor newsletter
def send_email_newsletter_doctor_verification(user):
    token = user.get_email_token()
    send_email('Confirm Your Email Address', 
                sender=current_app.config['ADMINS'][0], 
                recipients=[user.email], 
                text_body=render_template('email/verify_newsletter_doctor_email.txt', 
                                            user=user, 
                                            token=token), 
                html_body=render_template('email/verify_newsletter_doctor_email.html', 
                                            user=user, 
                                            token=token))


def send_new_password_email(user):
    token = user.get_email_token()
    send_email('Set New Password',
                sender=current_app.config['ADMINS'][0], 
                recipients=[user.email], 
                text_body=render_template('email/new_password.txt', 
                                            user=user, 
                                            token=token),
                html_body=render_template('email/new_password.html', 
                                            user=user, 
                                            token=token))


def send_password_changed_email(user):
    send_email('Your Password Has Been Changed',
                sender=current_app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/password_changed.txt', 
                                            user=user),
                html_body=render_template('email/password_changed.html', 
                                            user=user))


# thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Thread
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
