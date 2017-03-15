# reposter

This script dredges up an old repost from a subreddit of your choosing, makes sure it's at least 200 days old, and reposts it on your account. Good for karma farming.

It WILL NOT work on new accounts; Reddit's spam filter will automatically block your posts. However, it will work on an already established account that you have succesfully posted/commented/lurked from for at least, say, a month or so.

* * *

To use:
1. Log in to your account at reddit.com
2. Go to [your app preferences](https://www.reddit.com/prefs/apps)
3. Click the "Create a new app" button at the bottom of the page.
4. Choose the *script* option as the app type.
5. Set the *redirect uri* option as http://www.example.com/unused/redirect/uri 
6. Set the other options to whatever you want.
7. Download repost.py
8. Open repost.py in a text editor, and fill in your new app's information into the global variables `client_id` and `client_secret`
9. Write your username and password into the global variables `username` and `password`
10. Run the script with the first CLI arg as the subreddit you want to post to. Ex: `python repost.py funny`
11. Profit.

* * *

I built this after reading through [OAuth Quick Start](https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example) and the [Official Reddit API docs](https://www.reddit.com/dev/api/) -- and, of course, a lot of googling and Stack Overflow.
