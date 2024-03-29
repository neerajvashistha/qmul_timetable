import configparser
import datetime
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

import numpy as np
import cv2
import pyautogui

config = configparser.ConfigParser()
config.read("mail.conf")
MY_ADDRESS = config.get('email', 'username')
PASSWORD = config.get('email', 'password')
hostname = config.get('email', 'host')

# take screenshot using pyautogui
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image),
                     cv2.COLOR_RGB2BGR)
   
# writing it to the disk using opencv
cv2.imwrite("image1.png", image)

calendar_file = 'calendar'+str(datetime.datetime.today().strftime("%d-%m-%Y"))+'.csv'

def get_contacts(filename):
	"""
	Return two lists names, emails containing names and email addresses
	read from a file specified by filename.
	"""
	
	names = []
	emails = []
	with open(filename, mode='r', encoding='utf-8') as contacts_file:
		for a_contact in contacts_file:
			names.append(a_contact.split()[0])
			emails.append(a_contact.split()[1])
	return names, emails

def read_template(filename):
	"""
	Returns a Template object comprising the contents of the 
	file specified by filename.
	"""
	
	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

def main():
	names, emails = get_contacts('mycontacts.txt') # read contacts
	message_template = read_template('message.txt')

	# set up the SMTP server
	s = smtplib.SMTP(host=hostname, port=2525)
	s.starttls()
	print(MY_ADDRESS,PASSWORD)
	s.login(MY_ADDRESS, PASSWORD)

	# For each contact, send the email:
	for name, email in zip(names, emails):
		msg = MIMEMultipart()	   # create a message

		# add in the actual person name to the message template
		message = message_template.substitute(PERSON_NAME=name.title())

		# Prints out the message body for our sake
		print(message)

		# setup the parameters of the message
		msg['From']=MY_ADDRESS
		msg['To']=email
		msg['Subject']="This is TEST"
		
		# add in the message body
		msg.attach(MIMEText(message, 'plain'))
		
		files = ["image1.png"]
		for f in files or []:
			with open(f, "rb") as fil:
				part = MIMEApplication(
					fil.read(),
					Name=basename(f)
				)
			# After the file is closed
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)
		# send the message via the server set up earlier.
		s.send_message(msg)
		del msg
		
	# Terminate the SMTP session and close the connection
	s.quit()
	

main()
