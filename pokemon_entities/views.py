import folium

from django.db.models import Prefetch
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon.entities.active():
            add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon, pokemon.image_url(request))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append(
            {"pokemon_id": pokemon.id, "img_url": pokemon.image_url(request), "title_ru": pokemon.title}
        )

    return render(request, "mainpage.html", context={"map": folium_map._repr_html_(), "pokemons": pokemons_on_page})


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")

    img_url = pokemon.image_url(request)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entities.active().values("lat", "lon"):
        add_pokemon(folium_map, pokemon_entity["lat"], pokemon_entity["lon"], img_url)

    return render(
        request,
        "pokemon.html",
        context={"map": folium_map._repr_html_(), "pokemon": {"img_url": img_url, "title_ru": pokemon.title}},
    )
