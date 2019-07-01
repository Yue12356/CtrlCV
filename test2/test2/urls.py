"""test2 URL Configuration

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
from django.contrib import admin
from django.urls import path
import black.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', black.views.base, name='black_base'),
    path('about/', black.views.about, name='black_about'),
    path('player/', black.views.player, name='black_player'),
    path('services/', black.views.services, name='black_services'),
    path('player_query/', black.views.player_query, name='black_plary_query'),
    # path('chart_test/', black.views.ChartTest.as_view(), name='black_ChartTest'),
    path('chart_test/', black.views.chart_test, name='black_chart_test'),
    path('game2/', black.views.game2),
    path('team/', black.views.team),
    path('', black.views.home, name='black_home')
]
