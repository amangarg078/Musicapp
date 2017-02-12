# Musicapp

This is a django application that stores tracks and genres. User can see list of all tracks, search track by title, create and edit a track. Also, a user can see all the genres present, add and edit a genre.

Each action also has a corresponding REST Api which can be used to perform these operations.

<b>API Documentation</b>

Genre

List all Genres

Http GET to http://104.197.128.152:8000/v1/genres
```
{
    "count": 531,
    "next": "http://104.197.128.152:8000/v1/genres?page=2",
    "previous": null,
    "results": [
 
        {
            "id": 11,
            "name": "pop"
        },
        {
            "id": 19,
            "name": "hip hop"
        },
        {
            "id": 20,
            "name": "classical"
        },
        {
            "id": 21,
            "name": "indie-rock"
        }
    ]
}
```

Get single Genre record

Http GET to http://104.197.128.152:8000/v1/genres/11

```
{
    "id": 11,
    "name": "pop"
}
```


Edit Genre Record

Http POST to http://104.197.128.152:8000/v1/genres/11

Accepted response

```
{
    "id": 11,
    "name": "bollywood"
}
```


Create new Genre

Http POST to http://104.197.128.152:8000/v1/genres

Accepted response

```
{
    "name": "bollywood"
}
```


Track

List all Tracks

Http GET to http://104.197.128.152:8000/v1/tracks

```
{
    "count": 362,
    "next": "http://104.197.128.152:8000/v1/tracks?page=2",
    "previous": null,
    "results": [
        {
            "id": 38,
            "title": "Hey Jude",
            "rating": "4.9",
            "genres": [
                {
                    "id": 5,
                    "name": "ramesh"
                }
            ]
        },
        {
            "id": 39,
            "title": "hello adele",
            "rating": "4.0",
            "genres": [
                {
                    "id": 4,
                    "name": "bollywood"
                },
                {
                    "id": 8,
                    "name": "metakai"
                }
            ]
        },
        {
            "id": 43,
            "title": "Eshun EDM",
            "rating": "5.0",
            "genres": [
                {
                    "id": 6,
                    "name": "tap"
                }
            ]
        },
       
    ]
}
```


Search Tracks with title

Http GET to http://104.197.128.152:8000/v1/tracks?title=Hymn%20for%20the%20weekend

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 44,
            "title": "Hymn for the weekend",
            "rating": "1.0",
            "genres": [
                {
                    "id": 23,
                    "name": "new test"
                }
            ]
        }
    ]
}
```


Get single Track record

Http GET to http://104.197.128.152:8000/v1/tracks/44

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 44,
            "title": "Hymn for the weekend",
            "rating": "1.0",
            "genres": [
                {
                    "id": 23,
                    "name": "new test"
                }
            ]
        }
    ]
}
```

 
Edit Track Record

Http POST to http://104.197.128.152:8000/v1/tracks/1

Accepted response
```
{
    "id": 1,
    "title": "animals",
    "rating": 4.5,
    "genres": [
        1
    ]
}
```

Create new Track

Http POST to http://104.197.128.152:8000/v1/tracks

Accepted response
```
{
    "title": "animals",
    "rating": 4.5,
    "genres": [
        1
    ]
}
```

