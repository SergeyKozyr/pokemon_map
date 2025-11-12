from django.db import models
from django.db.models import Manager, QuerySet, Q
from django.http import HttpRequest
from django.utils.timezone import localtime


class PokemonEntityManager(Manager):
    def active(self) -> QuerySet:
        local_time = localtime()
        return self.exclude(Q(appeares_at__gt=local_time) | Q(disappeares_at__lte=local_time))


class Pokemon(models.Model):
    title = models.CharField("Название на русском", max_length=200)
    title_en = models.CharField("Название на английском", max_length=200, null=True, blank=True)
    title_jp = models.CharField("Название на японском", max_length=200, null=True, blank=True)
    image = models.ImageField("Изображение", null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        verbose_name="Из кого эволюционировал",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
    )

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self) -> str:
        return self.title

    def image_url(self, request: HttpRequest) -> str | None:
        return request.build_absolute_uri(self.image.url) if self.image else None


class PokemonEntity(models.Model):
    objects = PokemonEntityManager()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities", verbose_name="Покемон")
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeares_at = models.DateTimeField("Появляется в")
    disappeares_at = models.DateTimeField("Исчезает в")
    level = models.IntegerField("Уровень", default=1)
    health = models.IntegerField("Здоровье", default=1)
    damage = models.IntegerField("Атака", default=1)
    defence = models.IntegerField("Защита", default=1)
    stamina = models.IntegerField("Выносливость", default=1)

    class Meta:
        verbose_name = "Сущность покемона"
        verbose_name_plural = "Сущности покемонов"

    def __str__(self) -> str:
        return f"{self.pokemon.title} {self.level} уровня"
