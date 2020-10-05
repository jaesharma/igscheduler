import os,time,autoit,sys,random,json
import datetime as dt
from selenium import webdriver
from helpers import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

str_keys=["username","password","folder"]
int_keys=["pageindex","daystoskip"]

class Scheduler(object):
    def __init__(self):
        if not os.path.exists('./config.json'):
            print(f"Initial configuration file does not exist\n{'-'*12}\nsetting up configuration file")
            setInitials()
        self.config=getConfig()
        self.attempt=15
        self.fileCount=len(os.listdir(self.config["folder"]))
        self.captions=getCaptions()
        self.driver=webdriver.Chrome()

    def login(self):
        self.driver.maximize_window()
        try:
            self.driver.get(url)
            self.driver.find_element_by_xpath("//div[@id='u_0_0']/div[2]/div/div[2]/div/div/div/div[2]/div/div/span/div/div").click()
            self.driver.find_element_by_id('email').send_keys(self.config["username"])
            self.driver.find_element_by_id('pass').send_keys(self.config["password"])
            self.driver.find_element_by_id('loginbutton').click()
            time.sleep(1)
            self.driver.get(igurl)
            print("Logged in")
        except Exception as err:
            print("Login Failed\n",err)
            exit()

    def upload(self,path,date,h,m,ap):
        try:
            self.driver.find_elements_by_class_name('rwb8dzxj')[3].click() #create post button
            time.sleep(1)
            self.driver.find_elements_by_class_name('rwb8dzxj')[9].click() #instagram feed button
            time.sleep(2)
            element=self.driver.find_elements_by_class_name('_4ik4')[14+self.config['pageindex']] #page click
            self.driver.execute_script("arguments[0].click();",element)
            #caption
            element=self.driver.find_elements_by_class_name('_1mf')[0]
            #os.system(f"echo {captions[str(random.randint(0,len(captions)-1))]} | clip")
            time.sleep(1)
            #element.send_keys(Keys.CONTROL, 'v')
            element.send_keys(self.captions[str(random.randint(0,len(self.captions)-1))])
            self.driver.find_elements_by_class_name('_82ht')[0].click()
            # self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/div[1]/div/div[5]/div/div/div/span').click() #file upload button
            time.sleep(1)
            #Selenium only works on browser, 'upload window' is OS window, so i used autoit to control it.
            _attempt=4
            while _attempt:
                try:
                    self.driver.find_elements_by_class_name('_m')[0].click()
                    time.sleep(1)
                    autoit.win_activate("Open")
                    break
                except:
                    _attempt-=1

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
            self.driver.find_elements_by_class_name('_43rm')[3].click()   #schedule button 
            time.sleep(5)
            if os.path.splitext(path)[1]=='.mp4':
                time.sleep(5)
            self.attempt=15
        except KeyboardInterrupt:
            main()
        except Exception as e:
            print(e)
            self.attempt-=1
            if autoit.win_exists('Open'):
                autoit.win_close('Open')
            if self.attempt:
                self.driver.get(igurl)
                time.sleep(3)
                self.upload(self.getpost(),date,h,m,ap)
            else:
                self.err()

    def err(self):
        print("something went wrong, check connection and try again.")
        exit(0)

    def saveConfig(self):
        with open('config.json','w') as conf:
            json.dump(self.config,conf,indent=4)

    def schedule(self,path,date,h,m,ap):
        time.sleep(2)
        self.upload(path,date,h,m,ap)

    def getpost(self):
        index=int(random.randint(1,self.fileCount)%(self.fileCount))-1
        path=os.path.join(os.getcwd(),self.config["folder"])
        db=os.listdir(path)
        post=os.path.join(path,db[index])
        return post

    def scheduler(self):
        self.login()
        now=dt.datetime.now().date()+dt.timedelta(days=self.config["daystoskip"])
        iterator=180-self.config["daystoskip"]
        for x in range(iterator):
            datestr=(now+dt.timedelta(days=x)).strftime('%m/%d/%Y')
            print(datestr)
            self.schedule(self.getpost(),datestr,'9','15','a')
            self.schedule(self.getpost(),datestr,'11','15','a')
            self.schedule(self.getpost(),datestr,'01','15','p')
            self.schedule(self.getpost(),datestr,'5','15','p')
            self.schedule(self.getpost(),datestr,'8','25','p')
            self.config["daystoskip"]+=1
            self.saveConfig()
            self.config=getConfig()
            cls()

def setInitials():
        initials=dict()
        for key in str_keys:
            initials[key]=input(f'{key}: ')
        for key in int_keys:
            initials[key]=int(input(f'{key}: ') or '0')
            if key=="daystoskip" and not initials[key]:
                initials[key]=1
        with open('config.json','w') as fh:
            json.dump(initials,fh,indent=4)

def configuration():
    if not os.path.exists('./config.json'):
        setInitials()
    else:
        with open('config.json','r') as fh:
            configs=json.load(fh)
            for key in configs.keys():
                changes=input(f'\t\t{key}({configs[key]}): ')
                if changes:
                    configs[key]=int(changes) if key in int_keys else changes
            with open('config.json','w') as fh:
                json.dump(configs,fh,indent=4)

def addCaption():
    print("Enter caption(press 'ctrl+z & Enter' when you are done): ")
    newSet=sys.stdin.read()
    captions=getCaptions()
    captions[str(len(captions))]=newSet
    with open('captions.json','w') as fh:
        json.dump(captions,fh,indent=4)
    print("="*5,"caption added","="*5)
    time.sleep(.5)

def getCaptions():
    captions=dict()
    if os.path.exists('./captions.json'):
        with open('captions.json','r') as fh:
            captions=json.load(fh)
    if not len(captions):
        captions["0"]=""
    return captions

def getConfig():
    config=dict()
    with open('config.json','r') as fh:
        config=json.load(fh)
    return config

def main():
    while True:
        logo()
        print("\t\t1.Download\n\t\t2.Schedule\n\t\t3.Configure\n\t\t4.Add Caption\n\t\t5.Exit")
        choice=input("> ")
        if choice=='1':
            download()
        elif choice=='2':
            s=Scheduler()
            s.scheduler()
        elif choice=='3':
            configuration()
        elif choice=='4':
            addCaption()
        elif choice=='5':
            exit()

if __name__=='__main__':
    main()
