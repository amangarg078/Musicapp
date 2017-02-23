from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Tracks, Genres
from app.forms import QueryForm, TrackForm, GenreForm
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from rest_framework import filters
import requests
from django.core.urlresolvers import reverse
from .serializers import TrackSerializer, GenreSerializer, GetTrackSerializer
# Create your views here.

def get_pages(total):
    """
    Get total number of pages, 5 being set as default pages in settings.py
    """
    total_pages = (total / 5) + 1
    if total_pages > 1:
        has_other_pages = True
    else:
        has_other_pages = False
    return total_pages, has_other_pages


def get_pagination_fields(r):
    """
    Get pagination fields
    """
    pagination = {}
    next, prev = False, False
    if r.json()['next']:
        next = int(r.json()['next'].split('?page=')[1])
        current = next - 1

    if r.json()['previous']:
        prev_array = r.json()['previous'].split('?page=')
        if len(prev_array) == 1:
            prev = 1
        else:
            prev = int(prev_array[1])
        current = prev + 1

    pagination['next'] = next
    pagination['prev'] = prev
    pagination['current'] = current
    return pagination


def index(request):
    form = QueryForm()

    """
    Pagination and data view logic
    """
    host = request.get_host()
    page = request.GET.get('page')
    if page is not None:
        page = int(page)
    r = requests.get('http://%s/app/v1/tracks/' % host)
    total_pages, has_other_pages = get_pages(r.json()['count'])

    if total_pages >= page > 0:
        r = requests.get('http://%s/app/v1/tracks/?page=%d' % (host, page))
        result = r.json()['results']
    elif page < 0:
        r = requests.get('http://%s/app/v1/tracks/' % host)
        result = r.json()['results']
    elif page is None:
        r = requests.get('http://%s/app/v1/tracks/' % host)
        result = r.json()['results']
    else:
        r = requests.get('http://%s/app/v1/tracks/?page=%d' % (host, total_pages))
        result = r.json()['results']

    for i in result:
        i['rating'] = int(float(i['rating']))
        i['rating_empty'] = range(5 - i['rating'])
        i['rating'] = range(i['rating'])

    for i in result:
        lis = []
        for j in i['genres']:
            lis.append(j['name'])
        i['genre_list'] = " | ".join(lis)

    if request.GET.get('name'):
        name = request.GET.get('name')
        r = requests.get('http://%s/app/v1/tracks/?title=%s' % (host, name))
        result = r.json()['results']
        for i in result:
            i['rating'] = int(float(i['rating']))
            i['rating_empty'] = range(5 - i['rating'])
            i['rating'] = range(i['rating'])

        for i in result:
            lis = []
            for j in i['genres']:
                lis.append(j['name'])
            i['genre_list'] = " | ".join(lis)

        count = len(result)
        return render(request, 'app/index.html', {'result': result, 'count': count, 'form': form})
    count = len(result)

    total_pages = range(1, total_pages + 1)
    pagination = get_pagination_fields(r)
    pagination['total_pages'] = total_pages
    pagination['has_other_pages'] = has_other_pages

    return render(request, 'app/index.html',
                  {'form': form, 'count': count, 'result': result, 'pagination': pagination})


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
    """
    Pagination and data view logic
    """
    host = request.get_host()
    page = request.GET.get('page')
    if page is not None:
        page = int(page)
    r = requests.get('http://%s/app/v1/genres/' % host)
    total_pages, has_other_pages = get_pages(r.json()['count'])

    if total_pages >= page > 0:
        r = requests.get('http://%s/app/v1/genres/?page=%d' % (host, page))
        result = r.json()['results']
    elif page < 0:
        r = requests.get('http://%s/app/v1/genres/' % host)
        result = r.json()['results']
    elif page is None:
        r = requests.get('http://%s/app/v1/genres/' % host)
        result = r.json()['results']
    else:
        r = requests.get('http://%s/app/v1/genres/?page=%d' % (host, total_pages))
        result = r.json()['results']

    total_pages = range(1, total_pages + 1)
    pagination = get_pagination_fields(r)
    pagination['total_pages'] = total_pages
    pagination['has_other_pages'] = has_other_pages

    return render(request, 'app/genrelist.html', {'result': result, 'pagination': pagination})


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
