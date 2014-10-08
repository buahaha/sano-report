#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

def send_mail(html_file, sender, recipent, logo='logo.png', *args, **kwargs):
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEText import MIMEText
  from email.MIMEImage import MIMEImage
  from email.MIMEBase import MIMEBase

  # Define these once; use them twice!
  strFrom = sender
  strTo = recipent

  # Create the root message and fill in the from, to, and subject headers
  from datetime import date
  msgRoot = MIMEMultipart('text', 'html')
  msgRoot['Subject'] = "Raport {0}".format(date.today())
  msgRoot['From'] = strFrom
  msgRoot['To'] = strTo
  msgRoot.preamble = unicode('To jest raport dla Sano.')

  # Encapsulate the plain and HTML versions of the message body in an
  # 'alternative' part, so message agents can decide which they want to display.
  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgText = MIMEText('To jest alternatywny tekst wiadomości.', "utf-8")
  msgAlternative.attach(msgText)

  # Read html file and change logo image declaration
  html = ""
  import os.path
  assert os.path.isfile(html_file)
  with open(html_file, 'rb') as f:
    html = f.read()
    # import re
    # html = re.sub("logo.png", "cid:image1", temp)


  msgText = MIMEText(html, "html", "utf-8")
  msgAlternative.attach(msgText)

  # In case you need some of this functionality, please uncomment

  # We reference the image in the IMG SRC attribute by the ID we give it below
  # # This example assumes the image is in the current directory
  # assert os.path.isfile('logo.png')
  # fp = open('logo.png', 'rb')
  # msgImage = MIMEImage(fp.read())
  # fp.close()

  # # Define the image's ID as referenced above
  # msgImage.add_header('Content-ID', '<image1>')
  # msgRoot.attach(msgImage)

  # files = (html_file, logo)

  # for f in files:
  #   part = MIMEBase('application', "octet-stream")
  #   part.set_payload(open(f,"rb").read())
  #   Encoders.encode_base64(part)
  #   part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
  #   msgRoot.attach(part)

  # Send the email
  server = kwargs.get('server', 'localhost')
  user = kwargs.get('user', None)
  password = kwargs.get('password', None)
  import smtplib
  smtp = smtplib.SMTP()
  smtp.connect(server)
  # Authenticate if username present
  if (not user == None):
    smtp.login(user, password)
  smtp.sendmail(strFrom, strTo, msgRoot.as_string())
  smtp.quit()

