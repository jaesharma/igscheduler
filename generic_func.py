import random
import instaloader,time,os
from optparse import OptionParser

L = instaloader.Instaloader()

captions=[]

def getCaptions():
    if(not len(captions)):
        return "empty"
    return captions[random.randint(0,len(captions)-1)]

def addCaption(caption):
    captions.append(str(caption))

def download(instauser,count):
	c=0
	profile=instaloader.Profile.from_username(L.context,instauser)
	L.downlaod_videos=False
	L.download_video_thumbnails=False
	L.download_comments=False
	L.save_metadata=False
	L.compress_json=False
	L.post_metadata_txt_pattern=""
	for post in profile.get_posts():
		if c>int(count):
			break
		L.download_post(post,target=profile.username)
		c+=1
	print('done downloading ... fixing filename mess..wait...')
	time.sleep(1)
	os.chdir('./'+instauser)
	i=0
	for f in os.listdir():
		while True:
			if os.path.exists(str(i)+'.jpg') or os.path.exists(str(i)+'.mp4'):
				i+=1
			else:
				break
		fname,fext=os.path.splitext(f)
		if fext=='.jpg':
			os.rename(f,str(i)+'.jpg')
			i+=1
		elif fext=='.mp4':
			os.rename(f,str(i)+'.mp4')
			i+=1
		else:
			os.remove(f)

def cls():
	os.system('cls') if os.name=='nt' else os.system('clear')

def logo():
	cls()
	print('''	
		___  _  _ _    _  _    ____ ____ _  _ ____ ___  _  _ _    ____ ____
		|__] |  | |    |_/     [__  |    |__| |___ |  \ |  | |    |___ |__/
		|__] |__| |___ | \_    ___] |___ |  | |___ |__/ |__| |___ |___ |  \ 
\n\n''')
