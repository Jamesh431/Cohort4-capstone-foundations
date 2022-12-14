# Cohort4-capstone-foundations

Only need the 6 files uploaded to the github (all excluding erd, and both readme's), database will build itself. (ensure to use the pipfile uploaded, if not run following commands in terminal:
pipenv install
pipenv install bcrypt
pipenv install windows-curses
pipenv install tqdm
pipenv shell)

first time running main.py will bring up three prints in the terminal stating information for the database has been added. These only print when they are added the first time. 

When you run it the first time, all users have no password, and you will be asked to create a password for that user when signing in with their email at the beginning. Please read all prompts carefully

Recommendations:

For admin use, login with the email 'fake@admin.com'

for user use, login with the email 'fake@user.com'
(the user under that email already has a few recoreded assessment scores so they are ready to go to view their own assessments)


NOTE: Users can view their own assessment summary reports but cannot export them to a csv, admins can view assessment summary reports based on all users previous tests as well as viewing summary of all tests under a specific assessment and exporting that data to a csv as well. 

