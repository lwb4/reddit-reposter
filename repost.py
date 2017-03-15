# this script actually does work, I promise.
# Reddit's spam filter is pretty good, though, and will catch your posts if you are a new user.

# this isn't flawless, though -- it may help to invoke with "python -i repost.py" so Python drops 
# into a shell after the script runs. Good for stepping through, debugging etc. 

import requests
import requests.auth
import sys
import time
import re
from random import randint

# create an app on your account at https://www.reddit.com/prefs/apps
# enter your reddit app and account information here

client_id="your-client-id-goes-here"
client_secret="your-client-secret-goes-here"
username="your-account-username-goes-here"
password="your-account-password-goes-here"

# globals
now = time.time()
day_sec = 86400 # the number of seconds in a day
try:
    subreddit = sys.argv[1]
except IndexError:
    print "Usage: python repost.py nameOfSubreddit"
    exit()


# amp; appears to insert itself randomly in the URL
# get rid of it or the link won't work
def clean_url(url):
    return re.sub('amp;', '', url)

# automatically resubmit GET requests when you've been rate limited, maximum 5 times
# only suitable for GET requests that don't require authentication
def unlimit_request(url):
    response = requests.get(clean_url(url));
    i = 0
    while (response.status_code == 429 and i < 10):
        print "Rate limited on " + url
        print "Waiting one second..."
        time.sleep(1)
        response = requests.get(url)
        i = i + 1
    return response

# check if a given url has been posted in the last 200 days
def recently_posted(url):
    response = unlimit_request("https://reddit.com/r/" + subreddit + "/submit.json?url=" + url)
    
    try:
        posts = response.json()["data"]["children"]
    except TypeError:
        return False
    
    recent_post = False
    for post in posts:
        if ((now - post["data"]["created"])/day_sec < 200):
            recent_post = True
    return recent_post

# make a request to get the access token

client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": "RepostingClient/0.1 by YourUserName"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

# process the token

response_json = response.json()
access_token = response_json['access_token']
token_type = response_json['token_type']
headers = {"Authorization": token_type + " " + access_token, "User-Agent": "ChangeMeClient/0.1 by YourUserName"}

# make sure the subreddit they want a) exists, and b) allows link posts

response = unlimit_request("https://reddit.com/r/" + subreddit + "/about.json")
if (response.json()["data"]["submission_type"] == "self"):
    exit()

# # dig up an old post from top -> all time

response = unlimit_request("https://reddit.com/r/" + subreddit + "/top.json?sort=top&t=all&limit=100")
response_json = response.json()

# make sure the post is at least 200 days old
# also, make sure it is a link and not a self post

rand_i = randint(50,60)
post = response_json["data"]["children"][rand_i]
while (((now - post["data"]["created"])/day_sec < 200 
        or post["data"]["is_self"]
        or recently_posted(post["data"]["url"]))
        and rand_i < 99):
    rand_i = rand_i + 1
    post = response_json["data"]["children"][rand_i]

post_url = clean_url(post["data"]["url"])
post_title = post["data"]["title"]

# repost it

payload = {
    'title': post_title,
    'url': post_url, 
    'sr': subreddit, 
    'kind': 'link', 
    'resubmit': True
}
response = requests.post("https://oauth.reddit.com/api/submit", data=payload, headers=headers)

# check if the request was rate limited
response_str = response.json()["jquery"][20][3][0]
if (response_str != ''):
    print response_str # 'you are doing that too much'
else:
    print payload
    print response

