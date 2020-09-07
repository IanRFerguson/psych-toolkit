#!/usr/bin/env python
# coding: utf-8
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
smtp_server = 'smtp.gmail.com'                                              # Fill these in with your email + PW
my_address = ''
password = ''
cc = ''


# -------------- HELPER FUNCTIONS

def participantData():
    """
    Reads local XLSX file into Pandas DataFrame
    """

    all_participants = pd.read_excel('participantList.xlsx')

    # Replace null values with empty cells
    all_participants['Contacted'].fillna(0, inplace = True)
    all_participants['Date'].fillna(' ', inplace = True)
    all_participants['Time'].fillna(' ', inplace = True)
    all_participants['Responded'].fillna(' ', inplace = True)
    all_participants['Notes'].fillna(' ', inplace = True)

    return all_participants

def formatMessage(NAME):
    """
    Formats HTML email body with participant info
    Note - You'll want to change some of the text in here!
    """

    htmlBody = ("""
        <html>
        <head> </head>
        <body>
        <p> Hi """ + NAME + """,
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

    return htmlBody

def sendEmail(NAME, EMAIL):
    """
    Writes email to participant with text from formatMessage() function
    """

    # I can't remember why I defined this three different times lol
    now = datetime.datetime.now()

    # Text for the email itself
    messageText = formatMessage(NAME)

    # Format email itself (to/from/body/etc)
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = EMAIL
    msg['Cc'] = 'irf229@nyu.edu'
    msg['Subject'] = 'fMRI Study Recruitment'

    # Send that puppy!
    msg.attach(MIMEText(messageText, "html"))
    emailSetup.sendmail(from_addr= my_address, to_addrs = EMAIL, msg = msg.as_string())


def cleanUp(IX):
    """
    Converts remaining columns to string format, for excel's sake
    """

    pData["Contacted"].loc[IX] = str(now.strftime('%x')) + ' ' + str(now.strftime('%X'))
    pData["Date"].loc[IX] = str(" ")
    pData["Time"].loc[IX] = str(" ")

def toExcel():
    """
    Converts updated DataFrame back to XLSX format, saves it locally
    """

    header_list = []

    for col in pData:
        pattern = {'header':col}
        header_list.append(pattern)

    start = 'A1'
    end = 'G' + '' + str(len(pData['Participant Name']) + 1)
    tableSize = start + ':' + end

    manifest = xlsxwriter.Workbook('participantList.xlsx')
    main_sheet = manifest.add_worksheet('Participant Log')
    main_sheet.set_column('A:G', 28)
    main_sheet.add_table(tableSize, {'data': pData.stack(), 'columns':header_list})

    manifest.close()

# -------------- RIPPER
pData = participantData()

# Setup connection to gmail server with SMTPLib package
emailSetup = smtplib.SMTP(host = smtp_server, port = port)
emailSetup.ehlo()
emailSetup.starttls()
emailSetup.login(user = my_address, password = password)

# Loop through participant rows
for index, name in enumerate(pData["Participant Name"]):

    if name == ' ':                                                     # Skip blank rows
        continue

    if pData["Contacted"][index] == 0:                                  # Don't contact a participant > 1 time
        name = (re.findall('[A-Z][^A-Z]*', name))[0]                    # First name only
        sendEmail(name, pData["Participant Email"][index])              # Send email
        cleanUp(index)                                                  # Update other columns in participant row

        print("Contacting {}...".format(str(name)))                     # Print message to confirm
        sleep(5)                                                        # 5s lapse b/w participants

print("\n\nAll participants contacted")

# Push updated dataframe to Excel after all participants contacted
toExcel()
emailSetup.quit()
