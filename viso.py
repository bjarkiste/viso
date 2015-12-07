import requests
import re
import datetime
import time
import getpass


#This url will register you if followed
url = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&view=0&FagID=0&act=2&e='

nurl = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&sID=2&e='

username = input('Username: ')
password = getpass.getpass()

s = requests.get('https://myschool.ru.is/myschool', auth=(username, password)).content.decode('ISO-8859-1')

c = re.findall('<td.*?Page=Exe&ID=2.23&sID=2&e=.*?td>',s)

if len(c) == 0:
	print('There are no events available')
	exit()

#Display choices
print('The following events are available:')
for k,i in enumerate(c):
	i = re.search('title=\'.*?\'', i)
	print('  {} - {}'.format(k, i.group()[7:-1]))

#Pick something
choice = int(input('Choose an event: '))

try:
	c = c[choice]
	#Get the number
	num = re.search('ID=2&e=.*?\"', c).group()[7:-1]
except IndexError:
	print('That is an illegal choice, you dingus!')
	exit()

c = re.search('id\=\'personname\'\>\<span\>.*?\<\/span\>',s)
name = c.group().replace('id=\'personname\'><span>','').replace('</span>','')

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


date = datetime.datetime(int(y),int(m),int(d),int(h),int(minute))
date = date - datetime.timedelta(minutes=3)
print(date)

if datetime.datetime.now() < date: print('Will start spamming at: {}'.format(date))

#We wait until a few minutes before the registration to start spamming
now = datetime.datetime.now()
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
