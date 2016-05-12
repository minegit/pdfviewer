from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('ajax_upload_pdf', views.ajax_upload_pdf, name='ajax_upload_pdf'),
]
