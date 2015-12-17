import requests
import re
import datetime
import time
import getpass

#Probably want to replace all regex searches with soup
from bs4 import BeautifulSoup

#This url will register you if followed
url = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&view=0&FagID=0&act=2&e='
#This is the url to an event
nurl = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&sID=2&e='

username = input('Username: ')
password = getpass.getpass()

#Url to myschool frontpage used to find available events
s = requests.get('https://myschool.ru.is/myschool/?Page=Front', auth=(username, password)).content.decode('ISO-8859-1')

#Check if password is correct
soup = BeautifulSoup(s, 'html.parser')

if soup.find('title').contents[0][:3] == '401':
	print('Wrong username or password')
	exit()


c = re.findall('<td.*?Page=Exe&ID=2.23&sID=2&e=.*?td>',s)
if len(c) == 0:
	print('There are no events available')
	exit()

#List events
print('The following events are available:')
for k,i in enumerate(c):
	i = re.search('title=\'.*?\'', i)
	print('  {} - {}'.format(k, i.group()[7:-1]))

#Pick an event
try:
	choice = int(input('Choose an event: '))
except ValueError:
	print('Choose a number, you dingus!')
	exit()

try:
	c = c[choice]
	#Get the number
	num = re.search('ID=2&e=.*?\"', c).group()[7:-1]
except IndexError:
	print('That is an illegal choice, you dingus!')
	exit()

#Icelandic support by Kalli
soup = BeautifulSoup(s, 'html.parser')
name = soup.find('div', id='personname').contents[0].contents[0]
registration_string = 'Registration starts:' if soup.find('a', id='icelandicbtn') else 'Skráning hefst:'

#Find time and date and check if some dungus is already registered
s = requests.get(nurl+num, auth=(username, password)).content.decode('ISO-8859-1')

l = '\<strong\>%s\<\/strong\>' % name
c = re.search(l,s)
if c:
	print('You are already registered, you dingus!')
	exit(0)


#We find the date to register
soup = BeautifulSoup(s, 'html.parser')
datelis = [i for i in soup.find_all('tr') if i('div', class_='ruPanelsLabel')]

for i in datelis:
	div = i('div', class_='ruPanelsLabel')[0]
	if div.contents and registration_string in div.contents[0]:
		i = i.getText().replace(registration_string,'').strip()
		day, time = i.split()[1:]
		day = day.split('.')
		time = time.split(':')
		break


#We start spamming approximately 2 minutes before registration starts
date = datetime.datetime(int(day[2]),int(day[1]),int(day[0]),int(time[0]),int(time[1]))
date = date - datetime.timedelta(minutes=2)


now = datetime.datetime.now()
if now < date: print('Will start spamming at: {}'.format(date))
while now < date:
	time.sleep(10)
	now = datetime.datetime.now()


print('Starting registration spam')
#Cool kids use while 1
c = False
while not c:
	#Try to register
	s = requests.get(url+num, auth=(username, password)).content

	#We get some bytes back
	s = s.decode('ISO-8859-1')

	#Are we registered\?
	l = '\<strong\>%s\<\/strong\>' % name
	c = re.search(l,s)

print('Done, you should now be registered!')
