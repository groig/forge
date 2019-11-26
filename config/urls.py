"""forge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.urls import include, path
from django.views.generic import TemplateView

login_forbidden = user_passes_test(lambda u: u.is_anonymous, 'forge:index')
logout_forbidden = user_passes_test(lambda u: not u.is_anonymous, 'forge:index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forge/', include('forge.urls')),
    path('login/', login_forbidden(auth_views.login), {'template_name': 'forge/login.html'}, name='login'),
    path('logout/', logout_forbidden(auth_views.logout), {'template_name': 'forge/logged_out.html'}, name='logout'),
    path('404', TemplateView.as_view(template_name="404.html"), name="404"),
    path('jobs/', include('django_rq.urls')),
]
