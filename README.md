# psych-toolkit
Tools for participant recruitment, data analysis, etc. in academic psychology

## Recruitment
### automatedEmailReminder.py
- Allows user to quickly send reminders to multiple participants with different study times
- Different messages for weekday / weekend study times
- Note: Requires your email and password information to be updated

### batchRecruiter.py
- Use participantList.xlsx as template
- Input list of participants' names and emails
- Script will parse through list, email participants, and log
- Outputs .xlsx sheet in same format as template
- Note: Requires your email and password information to be updated

## Stimuli
### ensembleCodingConstructor.py
- Requires three directories: two for unique stimuli (e.g., black and white faces), one for output
- Main constructor function allows for user input 0-12 and unlimited iterations (e.g., 200 output arrays)
- For ensemble coding background literature see Alt, Goodale, Lick & Johnson (2018)
