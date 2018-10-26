from oauth.credentials import google_credentials
from google.auth.transport.requests import AuthorizedSession
from receipts.models import Receipts, Item, SyncInfo
import json
import base64
from datetime import datetime, timedelta

STORES = {'HMart': 'receipts@hmart.com'}

def sync(user):
    credentials = google_credentials[user]
    authed_session = AuthorizedSession(credentials)

    for key in STORES:
        name = key
        from_email = STORES[name]

        after = 'after:{0}'.format(get_last_sync(user))
        from_ = 'from:{0}'.format(from_email)
        query = '{0} {1}'.format(after, from_)

        parameter = {'q': query}
        response = authed_session.get(
            'https://www.googleapis.com/gmail/v1/users/me/messages', params=parameter)
        obj = json.loads(response.text)

        for msg in obj['messages']:
            parameter = {'format': 'raw'}
            response = authed_session.get(
                'https://www.googleapis.com/gmail/v1/users/me/messages/{0}'.format(msg['id']), params=parameter)
            write_message(user, name, response)

    update_last_sync(user, datetime.now())


def get_last_sync(user):
    try:
        sync = SyncInfo.objects.get(user=user)
    except SyncInfo.DoesNotExist:
        sync = None
    if sync:
        t = sync.time - timedelta(days=1)
        return t.strftime("%Y/%m/%d")
    return '1970/01/01'


def update_last_sync(user, time):
    SyncInfo.objects.update_or_create(user=user, time=datetime.strptime(time, '%Y/%m/%d'))


def write_message(user, name, response):
    obj = json.loads(response.text)
    raw = obj['raw']
    rc = base64.urlsafe_b64decode(raw).decode('unicode_escape')
    rdate = datetime.strptime(rc.split("\r\n")[2].strip(), '%a, %d %b %Y %H:%M:%S %z (%Z)')
    r = Receipts(receipts_name=name, receipts_date=rdate, raw_content=rc, user=user)
    r.save()
