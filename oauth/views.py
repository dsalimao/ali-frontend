from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from alifrontend import settings
from .credentials import google_credentials


from google_auth_oauthlib.flow import Flow

flow = Flow.from_client_secrets_file(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/gmail.readonly'],
    redirect_uri='http://localhost:8000/oauth/oauth_return')


def get_user(request):
    if 'google_user' in request.session:
        return JsonResponse({'payload': request.session['google_user']})
    return JsonResponse({'payload': 'Please Login'})


def start_oauth_flow(request):
    auth_url, _ = flow.authorization_url(prompt='consent')
    return JsonResponse({'payload': auth_url})


def oauth_return(request):
    code = request.GET['code']
    flow.fetch_token(code=code)

    session = flow.authorized_session()
    userinfo = session.get('https://www.googleapis.com/userinfo/v2/me').json()
    user_email = userinfo['email']
    google_credentials[user_email] = flow.credentials
    request.session['google_user'] = user_email

    return HttpResponseRedirect(reverse('receipts:index'))