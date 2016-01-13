from django.conf.urls import include, url
from lists import views

urlpatterns = [

    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/(\d+)/delete_item$', views.delete_item, name='delete_item'),
    url(r'^(\d+)/items/$', views.edit_list, name='edit_list'),
]
