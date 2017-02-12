from django import forms

from .models import Tracks, Genres


class QueryForm(forms.Form):
    name = forms.CharField(max_length=128)


class TrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control col-lg-8 '
            })

    class Meta:
        model = Tracks
        fields = ['title', 'rating', 'genres']


class GenreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control col-lg-8 '
            })

    class Meta:
        model = Genres
        fields = ['name']
