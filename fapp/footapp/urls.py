from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from footapp.views import teams_all, new_team, edit_team,delete_team, forum

from .views import PasswordResetView
from .views import mapa







urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('teamsall', views.teams_all, name="teams_all"),
    path('newteam', views.new_team, name="new_team"),
    path('jointeam/', views.join_team, name='join_team'),
    path('editteam/<int:id>', views.edit_team, name="edit_team"),
    path('deleteteam/<int:id>', views.delete_team, name="delete_team"),
    path('addpastmatch/', views.add_past_match, name='add_past_match'),
    path('recentmatches/', views.recent_matches, name='recent_matches'),
    path('leaguetable/', views.league_table, name='league_table'),
    path('yourteam/', views.your_team, name='your_team'),
    path('leave_team/<int:id>', views.leave_team, name='leave_team'),
    path('mapa/', mapa, name='mapa'),
    path('forum/', views.forum, name='forum'),
  



    path('password_reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)