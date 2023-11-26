from django.db import models
import secrets
from django.contrib.auth.models import User


def generate_random_key():
    return secrets.token_hex(4)

class Team(models.Model):
    name_team = models.CharField(max_length= 64, blank= False, unique= True)
    creation_date = models.DateField(null= True)
    id_league = models.PositiveSmallIntegerField(null= True)
    logo_team = models.ImageField(upload_to="logos", null= True, blank= True)
    city = models.CharField(max_length= 64, default="---")
    join_code = models.CharField(max_length=8, default= generate_random_key, unique= True)
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)


    def __str__(self):
        return self.name_team





class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
   


class Goal(models.Model):
    match = models.ForeignKey('PastMatch', related_name='goals', on_delete=models.CASCADE)
    scorer = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveSmallIntegerField()

class PlayerChange(models.Model):
    match = models.ForeignKey('PastMatch', related_name='player_changes', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_out = models.ForeignKey(Player, related_name='outgoing_changes', on_delete=models.CASCADE)
    player_in = models.ForeignKey(Player, related_name='incoming_changes', on_delete=models.CASCADE)
    minute = models.PositiveSmallIntegerField()

class PastMatch(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    date = models.DateField(null=True)
    score_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    score_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    goals_chances_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    goals_chances_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    shots_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    shots_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    shots_on_target_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    shots_on_target_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    free_kicks_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    free_kicks_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    penalty_kicks_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    penalty_kicks_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    Fouls_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    Fouls_team2 = models.PositiveSmallIntegerField(blank=False, default=0)
    Cards_team1 = models.PositiveSmallIntegerField(blank=False, default=0)
    Cards_team2 = models.PositiveSmallIntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.team1} vs. {self.team2}"
    


    













