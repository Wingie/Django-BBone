import urllib2
from oauth_hook import OAuthHook
import requests
import json
from proj.vim.models import VimeoUser

OAuthHook.consumer_key = '489e803878ab0be44d34b969d62a7b36a3129250'
OAuthHook.consumer_secret = '43b7be9049034688351bdf5e8568d757949f93da'
oauth_hook = OAuthHook('86376506b569583a82adc0a3f179d051', \
                                            '6825eb941fc81fc6ea9259f89bcf6698f6fea67b', header_auth=True)

def vimeo_api(url):
    url = 'http://vimeo.com/' + url
    client = requests.session(hooks={'pre_request': oauth_hook})
    response = client.get(url)
    # print response.content
    return json.loads(response.content)

def get_first_staffpick_or_none(usr):
    url = '/api/rest/v2?format=json&method=vimeo.videos.getAll&user_id=%s' % usr
    response =  vimeo_api(url)
    for vid in response['videos']['video']:
        u = "http://vimeo.com/channels/staffpicks/"+vid['id']
        r = requests.get(u)
        if r.status_code == 200:
            return u
    return '0'

def usr_info(usr):
    res = {}
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

def create_usr(usr):
    data = usr_info(usr)
    if data is None:
        return "user not exist"
    if VimeoUser.objects.filter(user_name=data['user_name']).count() != 0:
        return "User Already Exists."
    else:
        usr = VimeoUser(display_name=data['display_name'].encode('utf-8'),\
                                      user_name=data['user_name'].encode('utf-8'),\
                                      page_url=data['page_url'].encode('utf-8'))
        if data['is_pro'] == "1" or data['is_plus'] == "1":
            usr.is_pay = True
        if data['number_of_videos'] != "0":
            usr.has_videos = True
        if data['staffpick'] != "0":
            usr.has_staff_pick = True
        usr.save()
        return usr

# export PYTHONPATH='/home/wingston/local/py/vimeo-py/';export DJANGO_SETTINGS_MODULE='proj.settings'
if __name__ == '__main__':
    print  "**",create_usr('robertoajovalasit')
    # print  "**",get_first_staffpick_or_none('eterea')