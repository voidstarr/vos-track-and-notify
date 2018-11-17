from twitter_scraper import get_tweets
import requests
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

LASTCHECK = datetime.now() - timedelta(hours=1)

with open('config.json') as f:
    data = json.load(f)

ACCESS_TOKEN = data['pb_access_token']

def doVOSCheck():
    global LASTCHECK
    for tweet in get_tweets('JagexClock',pages=1):
        if tweet['text'].startswith('The Voice of Seren') and tweet['time'] > LASTCHECK and 'Amlodd' in tweet['text']:
            #push to phone
            send_notification_via_pushbullet('VOS',tweet['text'])
            print(tweet)
            break
    LASTCHECK = datetime.now()

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

sched.add_job(doVOSCheck, trigger='cron', hour='*', minute=1)
sched.start()
