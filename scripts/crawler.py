from vimeo import *
import simplejson

usr_list = set()
usr_list.add('smithjournal')

def get_users(usr):
    url = '/api/rest/v2?format=json&method=vimeo.videos.getAll&user_id=%s'%usr
    response =  vimeo_api(url)
    for vid in response['videos']['video']:
        print "#",vid['id']
        try:
            likers = vimeo_api('/api/rest/v2?format=json&method=vimeo.videos.getLikers&video_id=%s'%vid['id'])
            
            print "saw ",likers['likers']['on_this_page']
            if likers['likers']['on_this_page'] == "0":
                continue

            for likr in likers['likers']['user']:
                usr_list.add(likr['username'])
        except Exception as e:
            pass
        print len(usr_list)

if __name__ == '__main__':
    while len(usr_list) < 700: 
        get_users(usr_list.pop())

    with open('usrlist_'+str(len(usr_list))+'.json', 'wb') as fp:
        json.dump(list(usr_list), fp)

    