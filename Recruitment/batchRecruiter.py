# NOTE: This script requires an xlsx file named "participantList.xlsx" to run. I've included a template.

# Script will find any participant entries that have been contacted and email them

import pandas as pd
import datetime
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xlsxwriter

now = datetime.datetime.now()

port = 587
smtp_server = 'smtp.gmail.com'
my_address = input("Your email:\t\t")
password = input("Enter your password:\t\t") # Not necessary if running locally, of course
cc = 'irf229@nyu.edu'

emailSetup = smtplib.SMTP(host = smtp_server, port = port)
emailSetup.ehlo()
emailSetup.starttls()
emailSetup.login(user = my_address, password = password)

all_participants = pd.read_excel('participantList.xlsx')

all_participants['Contacted'].fillna(0, inplace = True)
all_participants['Date'].fillna('None Specified', inplace = True)
all_participants['Time'].fillna('None Specified', inplace = True)

for index, participant in enumerate(all_participants['Participant Name']):

    if all_participants['Contacted'][index] == 0:

        # Participant has not yet been contacted

        now = datetime.datetime.now()

        contact_name = participant
        contact_email = all_participants['Participant Email'][index]

        htmlBody = ("""
        <html>
        <head> </head>
        <body>
        <p> Hi """ + contact_name + """,
        <br> <br>
        I hope this message finds you well! Our records show that you have previously participated in a research study with the Social Cognitive and Neural Sciences Lab at NYU, and I'm contacting you to see if you'd like to participate in another one.
        <br> <br>
        We have several screening criteria for this study. You'll be eligible if you are:
        <br>
        - Right Handed <br>
        - Normal or Corrected-to-Normal Vision <br>
        - No history of Neurological Disease <br>
        - Not currently taking psychoactive medication <br>
        <br>
        <p> This particular study will last about 90 minutes, and we can offer <b>$Y</b> in compensation.
        If you think you might be interested, please feel free to <a href="mailto:irf229@nyu.edu"> contact me directly</a>. <br> <br>
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

        print("Contacting " + contact_name)
        all_participants.loc[index, 'Contacted'] = now.strftime('%x') + ' ' + now.strftime('%X')

        sleep(5)

emailSetup.quit()

header_list = []

for col in all_participants:
    pattern = {'header':col}
    header_list.append(pattern)

manifest = xlsxwriter.Workbook('participantList.xlsx')
main_sheet = manifest.add_worksheet('Participant Log')
main_sheet.set_column('A:E', 28)
main_sheet.add_table('A1:E31', {'data': all_participants.stack(), 'columns':header_list})

manifest.close()
