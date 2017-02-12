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

    result = Tracks.objects.all()
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

        result = Tracks.objects.filter(title__icontains=name)
        count=len(result)
        return render(request, 'app/index.html', {'result': result, 'count': count, 'form': form})
    count=len(result)
    return render(request, 'app/index.html', {'form': form, 'count': count, 'result': result})


def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            s = form.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            print form.errors
    else:
        form = TrackForm()
    return render(request, 'app/upload.html', {'form': form})


def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            s = form.save()

            return HttpResponseRedirect(reverse('genre_list'))
        else:
            print form.errors
    else:
        form = GenreForm()
    return render(request, 'app/addgenre.html', {'form': form})


def genrelist(request):
    result = Genres.objects.all()
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

def trackDetails(request,id):
    track=get_object_or_404(Tracks,pk=id)
    if request.method == "POST":
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = TrackForm(instance=track)
    return render(request,'app/trackdetails.html',{'track':track,'form':form})

def genreDetails(request,id):
    genre=get_object_or_404(Genres,pk=id)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('genre_list'))
    else:
        form = GenreForm(instance=genre)
    return render(request,'app/genredetails.html',{'genre':genre,'form':form})


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genre to be viewed or edited.
    """
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenreSerializer


class TracksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genre to be viewed or edited.
    """
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title',)
    queryset = Tracks.objects.all().order_by('id')
    serializer_class = TrackSerializer


'''
obsolete views

@api_view(['GET', 'POST'])
def track_list(request):
    """
    List all tasks, or create a new track.
    """
    if request.method == 'GET':
        tracks = Tracks.objects.all()

        """
        Filtering on track title
        """
        title = request.query_params.get('title', None)
        if title is not None:
            tracks = tracks.filter(title__icontains=title)
        serializer = GetTrackSerializer(tracks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def track_detail(request, pk):
    """
    Get, udpate a specific track
    """
    try:
        tracks = Tracks.objects.get(pk=pk)
    except Tracks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetTrackSerializer(tracks)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TrackSerializer(tracks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''