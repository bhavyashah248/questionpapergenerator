from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^BSform/$', views.BSform, name='BSform'),
    url(r'^Auth/$', views.Auth, name='auth'),
    url(r'^Auth/Home/$', views.Home, name='home'),
    url(r'^logout/$', views.lout, name='logout'),
    url(r'^test/$', views.addq, name='test'),
    url(r'^addquestion/$', views.addq, name='test'),
    url(r'^submit/$', views.sub, name='sub'),
    url(r'^genpaper/$', views.gen, name='gen'),
    url(r'^result/$', views.result, name='result'),
    url(r'^populate/$', views.populate, name='populate'),
]