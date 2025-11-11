from django.contrib import admin

from pokemon_entities.models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    pass
