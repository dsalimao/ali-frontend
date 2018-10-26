from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect
from alifrontend import settings
from .credentials import google_credentials


from google_auth_oauthlib.flow import Flow

flow = Flow.from_client_secrets_file(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/gmail.readonly'],
    redirect_uri='http://localhost:8000/oauth/oauth_return')

def start_oauth_flow(request):
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


def oauth_return(request):
    code = request.GET['code']
    user = request.user
    print(user)

    flow.fetch_token(code=code)

    # You can use flow.credentials, or you can just get a requests session
    # using flow.authorized_session.
    session = flow.authorized_session()
    userinfo = session.get('https://www.googleapis.com/userinfo/v2/me').json()
    user_email = userinfo['email']
    google_credentials[user_email] = flow.credentials
    return HttpResponseRedirect(reverse('receipts:index'))