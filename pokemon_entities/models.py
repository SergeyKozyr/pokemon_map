from django.db import models
from django.db.models import Manager, QuerySet, Q
from django.http import HttpRequest
from django.utils.timezone import localtime


class PokemonEntityManager(Manager):
    def active(self) -> QuerySet:
        local_time = localtime()
        return self.exclude(Q(appeares_at__gt=local_time) | Q(disappeares_at__lte=local_time))


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def image_url(self, request: HttpRequest) -> str | None:
        return request.build_absolute_uri(self.image.url) if self.image else None


class PokemonEntity(models.Model):
    objects = PokemonEntityManager()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities")
    lat = models.FloatField()
    lon = models.FloatField()
    appeares_at = models.DateTimeField()
    disappeares_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    damage = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)
