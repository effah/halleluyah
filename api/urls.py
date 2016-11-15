from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import user_view, post_view

urlpatterns = [
    url(r'^users/$', user_view.UserList.as_view()), 
    url(r'^users/(?P<token>[-\w]+)/$', user_view.UserDetail.as_view()),
    url(r'^posts/$', post_view.PostList.as_view()),
    url(r'^posts/(?P<pk>\d+)/$', post_view.PostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)