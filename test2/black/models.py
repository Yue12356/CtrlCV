from django.db import models

class PlayerInfo(models.Model):
    name_game = models.CharField(max_length = 120, primary_key=True)#md5(name+game)
    player_name = models.CharField(max_length = 120)
    game_time = models.DateField()
    position=models.CharField(max_length = 4)
    time = models.PositiveSmallIntegerField()
    two_hit = models.PositiveSmallIntegerField()
    two_shot = models.PositiveSmallIntegerField()
    three_hit = models.PositiveSmallIntegerField()
    three_shot = models.PositiveSmallIntegerField()
    penalty_hit = models.PositiveSmallIntegerField()
    penalty_shot = models.PositiveSmallIntegerField()
    front = models.PositiveSmallIntegerField()
    back = models.PositiveSmallIntegerField()
    bord = models.PositiveSmallIntegerField()
    sup = models.PositiveSmallIntegerField()
    foul = models.PositiveSmallIntegerField()
    ST = models.PositiveSmallIntegerField()
    miss = models.PositiveSmallIntegerField()
    block = models.PositiveSmallIntegerField()
    point = models.PositiveSmallIntegerField()
    ZF = models.SmallIntegerField()
    first = models.PositiveSmallIntegerField()
    team_name = models.CharField(max_length = 120)
    HA = models.SmallIntegerField()
    A_point = models.SmallIntegerField()
    H_point = models.SmallIntegerField()
    two_rate = models.DecimalField(max_digits = 3, decimal_places = 2)
    three_rate = models.DecimalField(max_digits = 3, decimal_places = 2)
    penalty_rate = models.DecimalField(max_digits = 3, decimal_places = 2)
    wining = models.SmallIntegerField()
    class Meta:
        db_table = 'playerinfo'
        managed = True
        verbose_name = 'black'
        verbose_name_plural = 'blacks'
        ordering = ['game_time']
# Create your models here.

class teamInfo(models.Model):
    index = models.IntegerField(primary_key=True)
    game_time = models.DateField()
    two_hit = models.SmallIntegerField()
    two_shot = models.SmallIntegerField()
    three_hit = models.SmallIntegerField()
    three_shot = models.SmallIntegerField()
    penalty_hit = models.SmallIntegerField()
    penalty_shot = models.SmallIntegerField()
    front = models.PositiveSmallIntegerField()
    back = models.PositiveSmallIntegerField()
    bord = models.PositiveSmallIntegerField()
    foul = models.PositiveSmallIntegerField()
    miss = models.SmallIntegerField()
    block = models.SmallIntegerField()
    point = models.SmallIntegerField()
    team_name = models.CharField(max_length = 120)
    wining = models.SmallIntegerField()
    class Meta:
        db_table = 'teaminfo'
        managed = False
        verbose_name = 'black'
        verbose_name_plural = 'blacks'
        ordering = ['game_time']

