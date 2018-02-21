from django.contrib.auth.views import login, logout
from django.conf.urls import url
from accounts.views import signup

app_name = 'accounts'

urlpatterns = [
    url(r'^login/', login, {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^logout/', logout, {'next_page': '/'}, name="logout"),
    url("signup", signup, name="signup")
]