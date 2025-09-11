from django.urls import path
from authentications import views as authentications_view


appname = 'userauths'

urlpatterns = [
    path("/", authentications_view.index, name="")
]