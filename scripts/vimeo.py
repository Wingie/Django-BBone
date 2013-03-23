import urllib2
from oauth_hook import OAuthHook
import requests
import json
OAuthHook.consumer_key = '489e803878ab0be44d34b969d62a7b36a3129250'
OAuthHook.consumer_secret = '43b7be9049034688351bdf5e8568d757949f93da'
oauth_hook = OAuthHook('86376506b569583a82adc0a3f179d051', \
                                            '6825eb941fc81fc6ea9259f89bcf6698f6fea67b', header_auth=True)

def vimeo_api(url):
    url = 'http://vimeo.com/' + url
    client = requests.session(hooks={'pre_request': oauth_hook})
    # response = client.get('http://vimeo.com/api/rest/v2?format=json&method=vimeo.videos.getLikers&video_id=57125220')
    response = client.get(url)
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
    res['username']  = response['person']['username']
    res['display_name']  = response['person']['display_name']
    res['profileurl']  =response['person']['profileurl']
    res['is_plus'] = response['person']['is_plus']
    res['is_pro'] = response['person']['is_pro']
    res['is_staff'] = response['person']['is_staff']
    res['number_of_videos'] = response['person']['number_of_videos']
    res['staffpick'] = get_first_staffpick_or_none(res['username'])
    # print  response['person']['number_of_videos']
    return res


if __name__ == '__main__':
    print  "**",usr_info('luisg8a')
    # print  "**",get_first_staffpick_or_none('eterea')