from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import user_view 

urlpatterns = [
    url(r'^users/$', user_view.UserList.as_view()), 
    url(r'^users/(?P<token>[-\w]+)/$', user_view.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)