from collections import Counter
from string import punctuation
import json
import html
import re
import requests
    

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

    
def check_group(group):
    params = {'count':1,
              'domain':group}
    res = vk_api('wall.get',**params)
    if 'error' in res:
        print(res)
        return [('error',res['error']['error_msg'])]
    else:
        return 1

        
def get_n_posts(group):
    params = {'count':1,
              'domain':group}
    res = vk_api('wall.get',**params)['response'][0]
    return res

    
def get_posts_as_one(group):
    posts = min(1000,get_n_posts(group))
    i = 0
    res = []
    while i <= posts+100:
        params = {'count':100,
                  'domain':group,
                  'offset':min(i,posts),
                  'fields':['text']}
        res += vk_api('wall.get',**params)['response'][1:]
        i += 100
    return ' '.join([x['text'] for x in res])

   
def count_wordforms(text):
    text = re.sub('<.*?>','',text)
    text = html.unescape(text)
    words = [x.lower().strip().strip(punctuation) for x in text.split()]
    words = [x for x in words if x.strip() not in punctuation+'—–']
    words_count = Counter(words)
    return words_count.most_common(100)

    
def vk_wordforms(group):
    ch = check_group(group)
    if ch == 1:
        t = get_posts_as_one(group)
        return count_wordforms(t),True
    else:
        return ch,False
