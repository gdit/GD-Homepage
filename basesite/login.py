from django.contrib.auth import authenticate, login, logout

def inside_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
    return user
  else:
    return None

def inside_logout(request):
  logout(request)
