import random
import instaloader,time,os
from optparse import OptionParser

L = instaloader.Instaloader()

colors={'red':'\033[5;31m','green':'\033[5;32m','yellow':'\033[5;33m','blue':'\033[5;34m','pink':'\033[5;35m','sky':'\033[5;36m','white':'\033[5;37m'}
url="https://facebook.com/creatorstudio"
igurl="https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=free_form_collection&content_table=INSTAGRAM_POSTS"


def download():
    username=input("Enter username: ")
    count=int(input("How many posts to download? : "))
    time.sleep(1)
    profile=instaloader.Profile.from_username(L.context,username)
    L.downlaod_videos=False
    L.download_video_thumbnails=False
    L.download_comments=False
    L.save_metadata=False
    L.compress_json=False
    L.post_metadata_txt_pattern=""
    for post in profile.get_posts():
        if not count:
            break
        L.download_post(post,target=profile.username)
        count-=1
    print('done downloading ... fixing filename mess..wait...')
    time.sleep(1)
    os.chdir('./'+username)
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
    os.chdir('../')
    print("--------------Downloading done------------")

def cls():
    os.system('cls') if os.name=='nt' else os.system('clear')

def logo():
    cls()
    print('''   
        ___  _  _ _    _  _    ____ ____ _  _ ____ ___  _  _ _    ____ ____
        |__] |  | |    |_/     [__  |    |__| |___ |  \ |  | |    |___ |__/
        |__] |__| |___ | \_    ___] |___ |  | |___ |__/ |__| |___ |___ |  \ 
\n\n''')
