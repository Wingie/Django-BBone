import urllib2
from oauth_hook import OAuthHook
import requests
import json
from vim.models import VimeoUser
import time
OAuthHook.consumer_key = '489e803878ab0be44d34b969d62a7b36a3129250'
OAuthHook.consumer_secret = '43b7be9049034688351bdf5e8568d757949f93da'
oauth_hook = OAuthHook('86376506b569583a82adc0a3f179d051', \
                                            '6825eb941fc81fc6ea9259f89bcf6698f6fea67b', header_auth=True)

def vimeo_api(url):
    url = 'http://vimeo.com/' + url
    client = requests.session(hooks={'pre_request': oauth_hook})
    headers = {
    'User-Agent': 'Mozilla 3.12',
    }
    response = client.get(url,headers=headers)
    # print response.content
    # print response.headers
    return json.loads(response.content)

def get_first_staffpick_or_none(usr):
    url = '/api/rest/v2?format=json&method=vimeo.videos.getAll&user_id=%s' % usr
    response =  vimeo_api(url)
    try:
        total = response['videos']['total']
        print "SFscan~",total
        for vid in response['videos']['video']:
            u = "http://vimeo.com/channels/staffpicks/"+vid['id']
            r = requests.get(u)
            if r.status_code == 200:
                return u
    except Exception as e:
        return '0'    
    return '0'

def usr_info(usr):
    res = {}
    try:
        url = '/api/rest/v2?format=json&method=vimeo.people.getInfo&user_id=%s' % usr
        response =  vimeo_api(url)
        res['user_name']  = response['person']['username']
        if response['person']['username'] == "user17234915":
            return None ## wtf. Vimeo returns my oauth account details instead of a 404 for authenticated calls.
        res['display_name']  = response['person']['display_name']
        res['page_url']  =response['person']['profileurl']
        res['is_plus'] = response['person']['is_plus']
        res['is_pro'] = response['person']['is_pro']
        res['is_staff'] = response['person']['is_staff']
        res['number_of_videos'] = response['person']['number_of_videos']
        res['staffpick'] = get_first_staffpick_or_none(res['user_name'])
        # print  response['person']['number_of_videos']
        return res
    except Exception:
        return None

def create_usr(usr):
    data = usr_info(usr)
    if data is None:
        return "user not exist/Error"
    if VimeoUser.objects.filter(user_name=data['user_name']).count() != 0:
        return "User Already Exists."
    else:
        usr = VimeoUser(display_name=data['display_name'],\
                                      user_name=data['user_name'],\
                                      page_url=data['page_url'])
        if data['is_pro'] == "1" or data['is_plus'] == "1":
            usr.is_pay = True
        if data['number_of_videos'] != "0":
            usr.has_videos = True
        if data['staffpick'] != "0":
            usr.has_staff_pick = True
        usr.save()
        return usr

# export PYTHONPATH='/home/wingston/local/py/vimeo-py/proj';export DJANGO_SETTINGS_MODULE='settings'
if __name__ == '__main__':
    # print  "**",create_usr('robertoajovalasit')
    # print  "**",get_first_staffpick_or_none('eterea')
    with open('usrlist_7288.json', 'rb') as fp:
        data = json.load(fp)
        i = 1
        for user_id in data[3284:]: # 850
            print i
            print create_usr(user_id)
            i+=1
            time.sleep(10+i%5)
        