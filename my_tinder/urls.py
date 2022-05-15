"""dating_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import index, registration, client_page, login_client, logout_client, clients_page


urlpatterns = [
    path('index/', index, name='index'),
    path('clients/create/', registration, name='registration'),
    path('login/', login_client, name='login'),
    path('logout/', logout_client, name='logout'),
    path('clients/<int:id>/', client_page, name='client_page'),
    path('clients/<int:id>/other_clients', clients_page, name='watch_clients')
]
