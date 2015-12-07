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
s = requests.get('https://myschool.ru.is/myschool', auth=(username, password)).content.decode('ISO-8859-1')

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
choice = int(input('Choose an event: '))

try:
	c = c[choice]
	#Get the number
	num = re.search('ID=2&e=.*?\"', c).group()[7:-1]
except IndexError:
	print('That is an illegal choice, you dingus!')
	exit()

soup = BeautifulSoup(s, 'html.parser')
name = soup.find('div', id='personname').contents[0].contents[0]

#Find time and date and check if some dungus is already registered
s = requests.get(nurl+num, auth=(username, password)).content.decode('ISO-8859-1')

l = '\<strong\>%s\<\/strong\>' % name
c = re.search(l,s)
if not c:
	print('You are already registered, you dingus!')
	exit(0)

kek = re.search('Registration starts(.\s)*',s).group()
print(kek)
c = re.search('\d+\.\d+\.\d+ \d+:\d+', s).group()
print(c)

exit()
#Datestuff
c1, c2 = c.split()
d,m,y = c1.split('.')
h,minute = c2.split(':')


#We start spamming approximately 3 minutes before registration starts
date = datetime.datetime(int(y),int(m),int(d),int(h),int(minute))
date = date - datetime.timedelta(minutes=3)
print(date)

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
