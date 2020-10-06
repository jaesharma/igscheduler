import os,time,autoit,sys,random,json,getpass,clipboard
import datetime as dt
from selenium import webdriver
from helpers import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Scheduler(object):
    def __init__(self):
        if not os.path.exists('./config.json'):
            print(colors['green'],f"Initial configuration file does not exist\n{'-'*12}\nsetting up configuration file",colors['white'],sep="")
            setInitials()
        self.config=getConfig()
        self.attempt=15
        try:
            self.fileCount=len(os.listdir(self.config["folder"]))
        except FileNotFoundError:
            print(colors['red'],"The folder in configuration does not exist, make sure you spell the folder name correct & it exist in current folder.\nReset the configurtion.",colors['white'],sep="")
            sys.exit(0)
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
            print(colors["green"],"Logged in",sep="")
        except Exception as err:
            print(colors["red"],"Login Failed\n",err)
            sys.exit()

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
            caption=""
            if len(self.captions):
                caption=self.captions[str(random.randint(0,len(self.captions)-1))]
            clipboard.copy(caption)
            element.send_keys(Keys.CONTROL, 'v')
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
            print(colors["red"],e,sep="")
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
        print(colors["red"],"something went wrong, check connection and try again.",sep="")
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
            print(colors["sky"],datestr,colors["white"],sep="")
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
    configs=dict()
    configs["username"]=input("Enter fb business account username: ")
    configs["password"]=getpass.getpass("fb business account password: ")
    configs["folder"]=input("Folder name which contains the posts: ")
    configs["pageindex"]=int(input("Index of page in creator studio panel: ") or 0)
    configs["daystoskip"]=int(input("How many days to skip from today(dafault 1,schedule from tomm.): ") or 1)
    with open('config.json','w') as fh:
        json.dump(configs,fh,indent=4)
    print(colors["yellow"],"="*5,"All set","="*5,colors["white"],sep="")
    time.sleep(.6)

def configuration():
    if not os.path.exists('./config.json'):
        setInitials()
    else:
        with open('config.json','r') as fh:
            configs=json.load(fh)
        configs["username"]=str(input(f"Enter fb business account username: ") or configs["username"])
        configs["password"]=str(getpass.getpass("fb business account password: ") or configs["password"])
        configs["folder"]=str(input("Folder name which contains the posts: ") or configs["folder"])
        configs["pageindex"]=int(input("Index of page in creator studio panel: ") or configs["pageindex"])
        configs["daystoskip"]=int(input("How many days to skip from today(dafault 1,schedule from tomm.): ") or configs["daystoskip"])
        with open('config.json','w') as fh:
            json.dump(configs,fh,indent=4)
    print(colors["green"],"="*5,"All set","="*5,colors["white"],sep="")
    time.sleep(.6)

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
