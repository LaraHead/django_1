from django.contrib import admin
from django.urls import path
from viptohmtl.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('viptohmtl/', index),

]