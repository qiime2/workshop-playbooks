#!/usr/bin/env python

import csv
import email
import email.mime.multipart
import email.mime.text
import os
import smtplib
import ssl
import sys


from shared import build_base_fn


MSG_SUBJ = """\
QIIME 2 Workshop => Here is your server login sheet (attached)
"""


MSG_BODY = """\
Hello! Please find attached a copy of your server login information, as well
as some reference material to keep on hand during the upcoming QIIME 2
workshop.

Please note, the server might not yet be accessible - we will cover logging
into the server on the first day of the workshop, so please don't worry if you
try to log in and it doesn't work. We just want to make sure you have the
material on hand now.

Thanks so much and see you soon!
"""


def build_pdf_fp(name, username, output_dir):
    base_fn = build_base_fn(name)
    pdf_fn = '%s-%s.pdf' % (base_fn, username)
    pdf_fp = os.path.join(output_dir, pdf_fn)

    return pdf_fp


def build_msg(sender_email, receiver_email, attachment_fp):
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = MSG_SUBJ
    msg.attach(email.mime.text.MIMEText(MSG_BODY, 'plain'))

    payload = email.mime.base.MIMEBase('application', 'octet-stream')
    with open(attachment_fp, 'rb') as fh:
        payload.set_payload(fh.read())
    email.encoders.encode_base64(payload)
    payload.add_header('Content-Disposition', 'attachment',
                       filename=os.path.basename(attachment_fp))
    msg.attach(payload)

    return msg.as_string()


if __name__ == '__main__':
    output_pdf_dir = sys.argv[1]
    roster = sys.argv[2]
    domain = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]
    port = int(sys.argv[6])
    sender_email = sys.argv[7]

    ctx = ssl.create_default_context()

    with smtplib.SMTP_SSL(domain, port, context=ctx) as server:
        server.login(user, password)

        with open(roster) as fh:
            reader = csv.reader(fh, delimiter=',')
            next(reader)  # skip first row

            for row in reader:
                # Name, Email, Cohort, Username, Password, + extra columns
                name, receiver_email, username = row[0], row[1], row[3]
                pdf_fp = build_pdf_fp(name, username, output_pdf_dir)
                print('mailing `%s` `%s`' % (receiver_email, pdf_fp))
                msg = build_msg(sender_email, receiver_email, pdf_fp)
                server.sendmail(sender_email, receiver_email, msg)
