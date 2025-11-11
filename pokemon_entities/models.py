from django.db import models
from django.http import HttpRequest


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def image_url(self, request: HttpRequest) -> str | None:
        return request.build_absolute_uri(self.image.url) if self.image else None


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeares_at = models.DateTimeField()
    disappeares_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    damage = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)
