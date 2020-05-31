import os,time,autoit,sys,json
import datetime as dt
from selenium import webdriver
from generic_func import download,cls,logo
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

global config
str_keys=["username","password","caption","folder","url","igurl"]
int_keys=["pageindex","daystoskip"]

class Scheduler(object):
    def __init__(self):
    	self.driver=webdriver.Chrome()
    
    def login(self):
    	try:
    	    self.driver.get(config["url"])
    	    self.driver.find_element_by_class_name('_43rm').click()
    	    self.driver.find_element_by_id('email').send_keys(config["username"])
    	    self.driver.find_element_by_id('pass').send_keys(config["password"])
    	    self.driver.find_element_by_id('loginbutton').click()
    	    time.sleep(1)
    	    self.driver.get(config["igurl"])
    	    print("Logged in")
    	except Exception as err:
    	    print("Login Failed\n",err)
    	    exit()
    
    def upload(self,path,date,h,m,ap):
    	try:
    	    self.driver.find_elements_by_class_name('_43rm')[0].click() #create post button
    	    self.driver.find_elements_by_class_name('_6ff7')[0].click() #instagram feed button
    	    time.sleep(2)
    	    element=self.driver.find_elements_by_class_name('_7pqd')[int(config["pageindex"])] #first page click
    	    self.driver.execute_script("arguments[0].click();",element)
    	    #caption
    	    element=self.driver.find_elements_by_class_name('_1mf')[0]
    	    element.send_keys(Keys.CONTROL, 'v')
    	    self.driver.find_elements_by_class_name('_3-99')[0].click() #file upload button
    	    time.sleep(1)
    	    #Selenium only works on browser, 'upload window' is OS window, so i used autoit to control it.
    	    t1=0
    	    while t1<4:
    	    	try:
    	    	    self.driver.find_elements_by_class_name('_m')[0].click()
    	    	    time.sleep(2)
    	    	    autoit.win_activate("Open")
    	    	    break
    	    	except:
    	    	    t1+=1
    	    if t1:
    	    	return False
    
    	    autoit.control_send("Open","Edit1",path)
    	    autoit.control_send("Open","Edit1","{ENTER}")
    	    time.sleep(1)
    	    self.driver.find_elements_by_class_name('_8122')[0].click()
    
    	    self.driver.find_elements_by_class_name('_kx6')[1].click()
    	    self.driver.find_elements_by_class_name('_58al')[1].click()
    	    self.driver.find_elements_by_class_name('_58al')[1].send_keys(date) #set date
    	    #set hour
    	    element=self.driver.find_elements_by_class_name('_4nx3')[0]
    	    actions=ActionChains(self.driver)
    	    actions.move_to_element(element).click().send_keys(h).perform()
    	    #set minute
    	    element=self.driver.find_elements_by_class_name('_4nx3')[1]
    	    actions=ActionChains(self.driver)
    	    actions.move_to_element(element).click().send_keys(m).perform()
    	    #set AM/PM
    	    element=self.driver.find_elements_by_class_name('_4nx3')[2]
    	    actions.move_to_element(element).click().send_keys(ap).perform()
    	    self.driver.find_elements_by_class_name('_43rl')[4].click()   #schedule button 
    	    time.sleep(3)
    	    return True
    	except Exception as e:
    	    print(e)
    	    return False
    
    def schedule(self,path,date,h,m,ap):
    	temp=0
    	while True:
    	    if(self.upload(path,date,h,m,ap)):
    	        break
    	    else:
    	        if autoit.win_exists('Open'):
    	        	autoit.win_close('Open')
    	        self.driver.get(config["igurl"])
    	        time.sleep(2)
    	        if temp>8:
    	        	exit(0)
    	        temp+=1
    
    def scheduler(self):
       self.login()
       i=50
       now=dt.datetime.now().date()+dt.timedelta(days=config["daystoskip"])
       path=os.path.join(os.getcwd(),config["folder"])
       db=os.listdir(path)
       #for x in range(180-config.daystoskip):
       for x in range(10):
           datestr=(now+dt.timedelta(days=x)).strftime('%m/%d/%Y')
           time.sleep(5)
           self.schedule(os.path.join(path,db[i]),datestr,'9','15','a')
           self.schedule(os.path.join(path,db[i+1]),datestr,'01','15','p')
           self.schedule(os.path.join(path,db[i+2]),datestr,'6','15','p')
           self.schedule(os.path.join(path,db[i+3]),datestr,'8','25','p')
           i+=4
           print(str(i))
           cls()
           print(str(i))

def download_():
    username=input("Enter username: ")
    count=input("How many posts to download? : ")
    download(username,int(count))
    print("--------------Downloading done------------")
    time.sleep(1)

def configuration():
    with open('config.json','r') as fh:
        curr_configs=json.load(fh)
        for key in curr_configs.keys():
            changes=input(f'{key}({curr_configs[key]}): ')
            if changes:
                curr_configs[key]=int(changes) if key in int_keys else changes
    with open('config.json','w') as fh:
        json.dump(curr_configs,fh,indent=4)
    os.system(f'echo {config["caption"]}|clip')
    print("ALL SET!!")

def set_initials():
    initials=dict()
    for key in str_keys:
        initials[key]=input(f'{key}: ')
    for key in int_keys:
        initials[key]=int(input(f'{key}: ') or '0')
    with open('config.json','w') as fh:
        json.dump(initials,fh,indent=4)

def main():
    global config
    if not os.path.exists('./config.json'):
        print(f"Initial configuration file does not exist\n{'-'*12}\nsetting up configuration file")
        set_initials()
    with open('config.json','r') as fh:
        config=json.load(fh)
    os.system(f'echo {config["caption"]}|clip')
    while True:
        logo()
        print("1.Download\n2.Schedule\n3.Configure\n4.Exit")
        choice=input("> ")
        if choice=='1':
            download_()
        elif choice=='2':
            s=Scheduler()
            s.scheduler()
        elif choice=='3':
            configuration()
        elif choice=='4':
            exit()
    
if __name__=='__main__':
    main()
