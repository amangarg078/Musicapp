from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Tracks, Genres
from app.forms import QueryForm, TrackForm, GenreForm
from rest_framework import viewsets
from django.http import HttpResponseRedirect
import re
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from .serializers import TrackSerializer, GenreSerializer, GetTrackSerializer
# Create your views here.
def index(request):
    form = QueryForm()
    count = -1
    host = request.get_host()
    r = requests.get('http://%s/app/v1/tracks/' % host)
    result = r.json()

    for i in result:
        i['rating'] = int(float(i['rating']))
        i['rating_empty'] = range(5 - i['rating'])
        i['rating'] = range(i['rating'])

    for i in result:
        list = []
        for j in i['genres']:
            list.append(j['name'])
        i['genre_list'] = " | ".join(list)

    paginator = Paginator(result, 5)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    if request.GET.get('name'):
        name = request.GET.get('name')
        # name=re.findall('\w+',name)
        r = requests.get('http://%s/app/v1/tracks/?title=%s' % (host, name))
        result = r.json()['results']
        count = len(result)
        return render(request, 'app/index.html', {'result': result, 'count': count, 'form': form})
    count = len(result)

    return render(request, 'app/index.html', {'form': form, 'count': count, 'result': result})


def add_track(request):
    host = request.get_host()
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            rating = form.cleaned_data['rating']
            genre_set = form.cleaned_data['genres']
            genres = []
            for i in genre_set:
                genres.append(i.id)
            r = requests.post('http://%s/app/v1/tracks/' % host,
                              data={'title': title, 'rating': rating, 'genres': genres})

            return HttpResponseRedirect(reverse('index'))
        else:
            print form.errors
    else:
        form = TrackForm()
    return render(request, 'app/upload.html', {'form': form})


def add_genre(request):
    host = request.get_host()
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            r = requests.post('http://%s/app/v1/genres/' % host, data={'name': name})
            return HttpResponseRedirect(reverse('genre_list'))
        else:
            print form.errors
    else:
        form = GenreForm()
    return render(request, 'app/addgenre.html', {'form': form})


def genrelist(request):
    host = request.get_host()
    r = requests.get('http://%s/app/v1/genres/' % host)
    result = r.json()
    paginator = Paginator(result, 5)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return render(request, 'app/genrelist.html', {'result': result})


def trackDetails(request, id):
    host = request.get_host()
    track = get_object_or_404(Tracks, pk=id)
    if request.method == "POST":
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            title = form.cleaned_data['title']
            rating = form.cleaned_data['rating']
            genre_set = form.cleaned_data['genres']
            genres = []
            for i in genre_set:
                genres.append(i.id)
            r = requests.put('http://%s/app/v1/tracks/' % host,
                             data={'title': title, 'rating': rating, 'genres': genres})

            return HttpResponseRedirect(reverse('index'))
    else:
        form = TrackForm(instance=track)
    return render(request, 'app/trackdetails.html', {'track': track, 'form': form})


def genreDetails(request, id):
    host = request.get_host()
    genre = get_object_or_404(Genres, pk=id)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            name = form.cleaned_data['name']
            r = requests.put('http://%s/app/v1/genres/%s/' % (host, id), data={'name': name})
            return HttpResponseRedirect(reverse('genre_list'))
    else:
        form = GenreForm(instance=genre)
    return render(request, 'app/genredetails.html', {'genre': genre, 'form': form})


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genre to be viewed or edited.
    """
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenreSerializer


class TracksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows track to be viewed or edited.
    """
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title',)
    queryset = Tracks.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GetTrackSerializer
        return TrackSerializer

