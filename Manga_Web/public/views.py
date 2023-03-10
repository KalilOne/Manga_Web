from math import ceil
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from public.sparql.sparql import Sparql


SITE_NAME = "Manga_Web"
spqr = Sparql()

# Page Home
def index(request):
    template = loader.get_template('index.html')
    context = {
        'title': SITE_NAME,
        'slider': spqr.get_slider_manga(),
        'last_updated': spqr.get_last_eight_mangas_publicated(),
        'most_volume': spqr.get_mangas_with_most_volume()
    }
    return HttpResponse(template.render(context, request))

# Page Manga List
def manga_list(request, page):
    template = loader.get_template('pages/list_mangas.html')

    nb_mangas = int(spqr.get_all_mangas_count())
    offset = 30
    context = {
        'title': SITE_NAME,
        'nb_mangas': str(nb_mangas),
        'mangas': spqr.get_all_mangas(page, offset),
        'pagination': {
            'current_page' : str(page),
            'last_page' : str(ceil(nb_mangas/offset)),
            'prev_page' : str(page-1) if page>1 else str(page),
            'next_page' : str(page+1) if page<ceil(nb_mangas/offset) else str(page),
        }
    }

    return HttpResponse(template.render(context, request))

# Page Manga Details
def manga_details(request, name):
    template = loader.get_template('pages/details_manga.html')
    context = {
        'title': SITE_NAME,
        'manga': spqr.get_manga_details(name),
    }
    return HttpResponse(template.render(context, request))

# Page Auteur List
def auteurs_list(request, page):
    nb_auteurs = int(spqr.get_all_mangas_count())
    offset = 30

    template = loader.get_template('pages/list_auteurs.html')
    context = {
        'title': SITE_NAME,
        'auteurs': spqr.get_all_authors(page, offset),
        'nb_auteurs': str(nb_auteurs),
        'pagination': {
            'current_page' : str(page),
            'last_page' : str(ceil(nb_auteurs/offset)),
            'prev_page' : str(page-1) if page>1 else str(page),
            'next_page' : str(page+1) if page<ceil(nb_auteurs/offset) else str(page),
        }
    }
    return HttpResponse(template.render(context, request))

# Page Auteur Details
def auteur_details(request, name):
    template = loader.get_template('pages/details_auteur.html')
    context = {
        'title': SITE_NAME,
        'author': spqr.get_author_detail(name)
    }
    print(context)
    return HttpResponse(template.render(context, request))


# Custom page 404
def error404(request, exeption):
    context = {
        'title': SITE_NAME
    }
    return render(request, 'error-404.html', context, status=404)