import argparse
import requests
import re
import datetime
import time
import getpass

def parse_arguments():
	parser = argparse.ArgumentParser(description='spams myschool until user is registered, waits until a few minutes before registration to start spamming')
	parser.add_argument('-u', metavar='Username', help='myschool username')
	parser.add_argument('-n', metavar='visoID', type=int, help='rightmost part of url')
	parser.add_argument('-y', metavar='year', type=int, default=2015, help='current year (default 2015)')
	parser.add_argument('-m', metavar='month', type=int, help='month of registration')
	parser.add_argument('-d', metavar='day', type=int, help='day of registration')
	parser.add_argument('--hour', metavar='hour', type=int, default='13', help='hour of registration (Default: 13)')
	parser.add_argument('--minute', metavar='minutes', type=int, default='37', help='minute of registration (Default: 37)')

	return parser.parse_args()


args= parse_arguments()

date = datetime.datetime(args.y, args.m, args.d, args.hour, args.minute)
date = date - datetime.timedelta(minutes=4)
print('Will start spamming at:')
print(date)

#This url will register you if followed
url = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&view=0&FagID=0&act=2&e=' + str(args.n)

nurl = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&sID=2&e=' + str(args.n)

username = args.u
password = getpass.getpass()

s = requests.get(nurl, auth=(username, password)).content.decode('ISO-8859-1')

c = re.search('id\=\'personname\'\>\<span\>.*?\<\/span\>',s)
name = c.group().replace('id=\'personname\'><span>','').replace('</span>','')

#Check if some dingus has run the script when already registered
l = '\<strong\>%s\<\/strong\>' % name
c = re.search(l,s)
if c:
	print('You are already registered, you dingus!')
	exit(0)

#We wait until a few minutes before the registration to start spamming
now = datetime.datetime.now()
while now < date:
	time.sleep(10)
	now = datetime.datetime.now()


print("Let\'s start spamming")
#Cool kids use while 1
c = False
while not c:
	#Try to register
	s = requests.get(url, auth=(username, password)).content

	#We get some bytes back
	s = s.decode('ISO-8859-1')

	#Are we registered\?
	l = '\<strong\>%s\<\/strong\>' % name
	c = re.search(l,s)

