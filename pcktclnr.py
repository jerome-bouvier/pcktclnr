import os
import datetime
import time
from pocket import Pocket, PocketException
import json

p = Pocket(
    consumer_key='your_key',
    access_token='your_token'
)

# Set time limitation @ 2 months from now
time_limit = datetime.date.today() - datetime.timedelta(3*365/12)

# Convert datetime to timestamp
t_limit = time.mktime(time_limit.timetuple())

# Fetch and save list of articles
try:
    with open('items', 'w') as f:
        f.write(json.dumps(p.retrieve(
            favorite=0, detailType='simple'), indent=4))
        print('data exported !')
except PocketException as e:
    print(e)

# Seek and clean
with open('items', 'r') as f:
    archived_msg = 0
    articles = json.load(f)

    if articles['status'] == 1:
        for v in articles['list']:
            if float(articles['list'][v]['time_updated']) > t_limit:
                p.archive(articles['list'][v]['item_id'])
                archived_msg += 1
    else:
        print('importation failed !')

os.remove('items')
if archived_msg != 0:
    print(str(archived_msg) + ' ' + 'articles archived')
else:
    print('it\'s all good')
