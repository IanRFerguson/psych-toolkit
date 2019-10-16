# NOTE: This script requires an xlsx file named "participantList.xlsx" to run. I've included a template.

# Script will find any participant entries that have been contacted and email them

import pandas as pd
import datetime
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xlsxwriter
import re

now = datetime.datetime.now()

port = 587
smtp_server = 'smtp.gmail.com'
my_address = input("Enter your email address\n")
password = input("Enter your password\n")
cc = 'irf229@nyu.edu'

emailSetup = smtplib.SMTP(host = smtp_server, port = port)
emailSetup.ehlo()
emailSetup.starttls()
emailSetup.login(user = my_address, password = password)

all_participants = pd.read_excel('participantList.xlsx')

all_participants['Contacted'].fillna(0, inplace = True)
all_participants['Date'].fillna('None Specified', inplace = True)
all_participants['Time'].fillna('None Specified', inplace = True)
all_participants['Responded'].fillna(' ', inplace = True)
all_participants['Notes'].fillna(' ', inplace = True)

for index, participant in enumerate(all_participants['Participant Name']):

    if all_participants['Contacted'][index] == 0:

        # Participant has not yet been contacted

        now = datetime.datetime.now()

        contact_first_name = (re.findall('[A-Z][^A-Z]*', participant))[0]
        contact_email = all_participants['Participant Email'][index]

        htmlBody = ("""
        <html>
        <head> </head>
        <body>
        <p> Hi """ + contact_first_name + """,
        <br> <br>
        I hope this message finds you well! Our records show that you have previously participated in a research study with the Social Cognitive and Neural Sciences Lab at NYU, and I'm contacting you to see if you'd like to participate in another one.
        <br> <br>
        Since this is a neuroimaging study using fMRI, we have several screening criteria to make sure that you're eligible to participate. Please confirm the following:
        <br><br>
        - You are right handed <br>
        - You have Normal or Corrected-to-Normal Vision <br>
        - You have no history of neurological disease <br>
        - You're not currently taking psychoactive medication <br>
        <br>
        <p> This particular study will last about 90 minutes, and we can offer <b>$60</b> in compensation.
        If you think you might be interested, please feel free to <a href="mailto:irf229@nyu.edu"> contact me directly</a> to set up an appointment time. We'll be scanning exclusively on the weekends between 11 AM and 4 PM, if that works for your schedule.<br> <br>
        Thanks so much, I'll look forward to hearing from you! <br><br>
        <b>Ian Richard Ferguson</b><br>
        Research Assistant | Social Cognitive and Neural Sciences Lab <br>
        4 Washington Place, New York, NY 10003 <br>
        </body>
        </html>""")

        emailSetup = smtplib.SMTP(host = smtp_server, port = port)
        emailSetup.ehlo()
        emailSetup.starttls()
        emailSetup.login(user = my_address, password = password)

        msg = MIMEMultipart()
        msg['From'] = my_address
        msg['To'] = contact_email
        msg['Cc'] = 'irf229@nyu.edu'
        msg['Subject'] = 'fMRI Study Recruitment'

        msg.attach(MIMEText(htmlBody, "html"))
        emailSetup.sendmail(from_addr= my_address, to_addrs = contact_email, msg = msg.as_string())

        print("Contacting " + contact_first_name)
        all_participants.loc[index, 'Contacted'] = str(now.strftime('%x')) + ' ' + str(now.strftime('%X'))

        sleep(5)

emailSetup.quit()

for index, p in enumerate(all_participants['Contacted']):

    all_participants['Contacted'].loc[index] = str(p)
    all_participants['Date'].loc[index] = str(p)


header_list = []

for col in all_participants:
    pattern = {'header':col}
    header_list.append(pattern)

manifest = xlsxwriter.Workbook('participantList.xlsx')
main_sheet = manifest.add_worksheet('Participant Log')
main_sheet.set_column('A:G', 28)
main_sheet.add_table('A1:G31', {'data': all_participants.stack(), 'columns':header_list})

manifest.close()
