from django.shortcuts import HttpResponse, reverse, redirect

# The Sign In Url to redirect to Outlook Login
from authentication.authhelper import get_signin_url

# Outlook gives us authorization code, we ask for a token from it
from authentication.authhelper import get_token_from_code

# The helper to get data from outlook like roll number, email, name
from authentication.outlookservice import get_me

def home(request):

  # Redirecting to gettoken view after authenticating
  redirect_uri = request.build_absolute_uri(
      reverse('authentication:gettoken'))

  # Building the sig in url
  sign_in_url = get_signin_url(redirect_uri)

  return HttpResponse('<a href="' + sign_in_url + '">Click here to sign in and test outlook OAuth2</a>')


# Add import statement to include new function

def gettoken(request):

  #################################
  # Set redirect after saving token
  redirect_url = None
  ################################


  # get Token from code
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('authentication:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']

  # Save the token in session
  request.session['access_token'] = access_token

  # redirect_url = request.session.get('redirect_url', None)
  
  if redirect_url is None:

    #####################
    # Get user from token
    user = get_me(access_token)

    return HttpResponse("Token: %s<br>Name: %s<br>Roll Number: %s<br> Mail: %s" % (access_token, user['displayName'], user['surname'], user['mail']))
  else: 
    return redirect(redirect_url)
