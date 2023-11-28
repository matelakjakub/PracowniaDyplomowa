from django.forms import ModelForm
from .models import Team, Player, PastMatch, ForumPost
from django import forms
from django.contrib.auth.models import User


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name_team', 'logo_team', 'city', 'join_code']
        labels = {
            'name_team': 'Nazwa drużyny',
            'logo_team': 'Logo drużyny',
            'city': 'Miasto',
            'join_code': 'Kod dołączenia'
        }


class JoinTeamForm(forms.Form):
    join_code = forms.CharField(max_length=20, label=('Kod dołączenia'))

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

class ForumPostEditForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']





class PastMatchForm(forms.ModelForm):
    class Meta:
        model = PastMatch
        fields = ['team1', 'team2', 'date', 'score_team1', 'score_team2', 'goals_chances_team1', 'goals_chances_team2', 'shots_team1', 'shots_team2', 'shots_on_target_team1', 'shots_on_target_team2', 'free_kicks_team1','free_kicks_team2','penalty_kicks_team1','penalty_kicks_team2', 'Fouls_team1', 'Fouls_team2', 'Cards_team1', 'Cards_team2']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='DD-MM-YYYY'),
        }

    






