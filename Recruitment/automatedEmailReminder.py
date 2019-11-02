# NOTE: This script gives you the option to send email reminders for weekday or weekend studies (if building is locked on the weekend)
# Make sure to input your email information (lines 79 + 80)!

import webbrowser
import smtplib
import ssl
import datetime
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

loopCheck = 'Y'

while loopCheck == 'Y':

        name = input('Name:\t\t\t')
        day = input('Day of the Week:\t')
        date = input('Date:\t\t\t')
        studyTime = input('Time:\t\t\t')
        participantEmail = input(str('Email:\t\t\t'))
        weekend = input(str('Weekend? (Y/N)\t\t'))

        print('...')
        sleep(1)

        # FOR WEEKEDAY STUDIES
        weekDayText = ("""
        <html>
          <head> </head>
          <body>
            <p> Hi """ + name + """, <br> <br>
              I hope this message finds you well! This is a reminder that you are scheduled
              to participate in an upcoming study with the Social Cogntive and Neural Sciences Lab. <br><br>
              <b> Date:     </b>    """ + day + ' ' + date + """ <br> <br>
              <b> Time:     </b>    """ + studyTime + """ <br> <br>
              <b> Location: </b>    Center for Brain Imaging | 4 Washington Place <br><br></p>

          <p> When you arrive, please check in at the Public Safety desk in the main lobby. We will meet you at the desk at the time of your study. <br>
              These sessions are very expensive to book, so, if you wouldn't mind, <b><i>please confirm the receipt of this message </i></b> so we know to expect you.<br><br>
              If you have any questions please feel free to <a href="mailto:irf229@nyu.edu"> contact me directly</a>. <br> <br>
              Thanks so much, <br><br>
              <b>Ian Richard Ferguson</b><br>
              Research Assistant | Social Cognitive and Neural Sciences Lab <br>
              4 Washington Place, New York, NY 10003 <br>
            </body>
        </html>""")

        # FOR WEEKEND STUDIES
        weekEndText = ("""
        <html>
          <head> </head>
          <body>
            <p> Hi """ + name + """, <br> <br>
              I hope this message finds you well! This is a reminder that you are scheduled
              to participate in an upcoming study with the Social Cogntive and Neural Sciences Lab. <br><br>
              <b> Date:     </b>    """ + day + ' ' + date + """ <br> <br>
              <b> Time:     </b>    """ + studyTime + """ <br> <br>
              <b> Location: </b>    Center for Brain Imaging | 4 Washington Place <br><br></p>

          <p> Since it's the weekend, the building will be locked when you arrive. Send me an email if you arrive early; otherwise, I'll meet you outside at the time of your study. <br>
              These sessions are very expensive to book, so, if you wouldn't mind, <b><i>please confirm the receipt of this message </i></b> so we know to expect you.<br><br>
              If you have any questions please feel free to <a href="mailto:irf229@nyu.edu"> contact me directly</a>. <br> <br>
              Thanks so much, <br><br>
              <b>Ian Richard Ferguson</b><br>
              Research Assistant | Social Cognitive and Neural Sciences Lab <br>
              4 Washington Place, New York, NY 10003 <br>
            </body>
        </html>""")

        if weekend == 'N':
            htmlBody = weekDayText

        elif weekend == 'Y':
            htmlBody = weekEndText

        # SMTP SETUP
        port = 587
        smtp_server = 'smtp.gmail.com'
        my_address = # YOUR EMAIL
        password = # YOUR PASSWORD
        receiver_address = [participantEmail, 'irf229@nyu.edu']
        cc = 'irf229@nyu.edu'

        s = smtplib.SMTP(host = smtp_server, port = port)
        s.ehlo()
        s.starttls()
        s.login(user = my_address, password = password)

        for k in receiver_address:
            msg = MIMEMultipart()
            msg['From'] = my_address
            msg['To'] = k
            msg['Cc'] = cc
            msg['Subject'] = (f"Upcoming Study Reminder: {day} {date}")

            msg.attach(MIMEText(htmlBody, "html"))
            s.sendmail(my_address, k, msg.as_string())

        s.quit()

        print(f"\n{name} has been contacted\n")

        sleep(2)

        loopCheck = input(str('\nMore participants? (Y/N)   '))
        print('\n')

print('All participants contacted')
