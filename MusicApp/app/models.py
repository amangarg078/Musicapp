from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Genres(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Tracks(models.Model):
    # id=models.AutoField(primary_key=True,default=1)
    title = models.CharField(max_length=128)

    rating = models.DecimalField(max_digits=2, decimal_places=1)
    genres=models.ManyToManyField(Genres,related_name='tracks')

    def __unicode__(self):
        return self.title

    @property
    def get_genre(self):
        list=[]
        for j in self.genres.all():
            list.append(j.name)
        genre_list=" | ".join(list)
        return genre_list

    @property
    def get_rating(self):
        return range(int(self.rating))

    @property
    def get_empty_rating(self):
        return range(5-int(self.rating))


