import os
import time
import autoit
import sys
import datetime as dt
import getpass
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

caption='''Follow @success_100x
.
||| daily motivational posts |||
.
#garyvee #askgaryvee #successtips #thinkandgrowrich #entrepreneurquotes #entrepreneurial 
#businessadvice #motivationalmonday #successquote #businessquote #grindmode #hustling 
#lawofvibration #thelawofattraction #selfdevelopment #tailopez #dailyquotes 
#successmindset #successfully #successtip #successcoach #successstory #successfull 
#successdriven #motivationquote #youngentrepreneurs
'''

url='https://business.facebook.com/creatorstudio/?reference=visit_from_seo&mode=instagram&tab=instagram_content_posts&collection_id=all_pages'

def login(username,password):
	driver.get(url)
	driver.find_element_by_class_name('_43rm').click()
	driver.find_element_by_id('email').send_keys(username)
	driver.find_element_by_id('pass').send_keys(password)
	driver.find_element_by_id('loginbutton').click()
	driver.get(url)

def upload(pindex,path,caption,date,h,m,ap):
	try:
		driver.find_elements_by_class_name('_43rm')[0].click() #create post button
		driver.find_elements_by_class_name('_6vpg')[0].click() #instagram feed button
		time.sleep(2)
		element=driver.find_elements_by_class_name('_7pqd')[int(pindex)] #first page click
		driver.execute_script("arguments[0].click();",element)
		element=driver.find_elements_by_class_name('_1mf')[0]
		actions=ActionChains(driver)
		actions.move_to_element(element).click().send_keys(caption).perform() #caption
		time.sleep(1)
		driver.find_elements_by_class_name('_3-99')[0].click() #file upload button
		time.sleep(1)
		#Selenium only works on browser, 'upload window' is OS window, so i used autoit to control it.
		t1=0
		while True:
			try:
				driver.find_elements_by_class_name('_m')[0].click()
				time.sleep(2)
				autoit.win_activate("Open")
				break
			except:
					t1+=1
					if t1>4:
						return False

		autoit.control_send("Open","Edit1",path)
		autoit.control_send("Open","Edit1","{ENTER}")
		time.sleep(1)
		driver.find_elements_by_class_name('_8122')[0].click()

		driver.find_elements_by_class_name('_kx6')[1].click()
		driver.find_elements_by_class_name('_58al')[1].click()
		driver.find_elements_by_class_name('_58al')[1].send_keys(date) #set date
		#set hour
		element=driver.find_elements_by_class_name('_4nx3')[0]
		actions=ActionChains(driver)
		actions.move_to_element(element).click().send_keys(h).perform()
		#set minute
		element=driver.find_elements_by_class_name('_4nx3')[1]
		actions=ActionChains(driver)
		actions.move_to_element(element).click().send_keys(m).perform()
		#set AM/PM
		element=driver.find_elements_by_class_name('_4nx3')[2]
		actions.move_to_element(element).click().send_keys(ap).perform()
		driver.find_elements_by_class_name('_271k')[3].click()   #schedule button 
		time.sleep(2)
		return True
	except Exception as e:
		print(e)
		return False


def schedule(pindex,path,caption,date,h,m,ap):
	temp=0
	while True:
		if(upload(pindex,path,caption,date,h,m,ap)):
			break
		else:
			if autoit.win_exists('Open'):
				autoit.win_close('Open')
			time.sleep(2)
			driver.get(url)
			if temp>8:
				exit(0)
			temp+=1



# opt parser commands
parser=OptionParser()
parser.add_option('-u','--username',dest="username",help="facebook profile name")
parser.add_option('-p','--password',dest="password",help="facebook profile password")
parser.add_option('-t','--tag',dest="tag",help="instagram username")
parser.add_option('-f','--folder',dest="foldername",help="Specify folder name which have all posts (must be in current directory)")
parser.add_option('-i','--index',dest="pageindex",help="page index in facebook creator studio")
(option,args)=parser.parse_args()

# Driver code
i=0
now=dt.datetime.now().date()+dt.timedelta(days=1)
foldername=option.foldername
pageindex=option.pageindex
tag=option.tag


path=os.path.join(os.getcwd(),foldername)
db=os.listdir(path)

driver=webdriver.Chrome()
login(option.username,option.password)

for x in range(180):
	datestr=(now+dt.timedelta(days=x)).strftime('%m/%d/%Y')
	time.sleep(5)
	schedule(pageindex,os.path.join(path,db[i]),caption,datestr,'9','15','a')
	schedule(pageindex,os.path.join(path,db[i+1]),caption,datestr,'01','15','p')
	schedule(pageindex,os.path.join(path,db[i+2]),caption,datestr,'6','15','p')
	schedule(pageindex,os.path.join(path,db[i+3]),caption,datestr,'9','15','p')
	i+=4
	print(str(i))
os.system('cls')
print(str(i))
