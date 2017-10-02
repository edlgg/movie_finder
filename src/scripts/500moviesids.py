import tmdbsimple as tmdb
tmdb.API_KEY = 'f1a02539ea044b6d67a19c6bb2025b94'


## get list of movie ids
movie_ids = []
for i in range(1,26,1):
    discover = tmdb.Discover()
    response = discover.movie(page=i, sort_by='popularity.desc')
    for s in discover.results:
        movie_ids.append(s['id'])


    








