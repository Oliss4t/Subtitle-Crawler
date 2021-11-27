from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()

# get a movie
def get_movie():
#movie = ia.get_movie('0133093')
    movies = ia.search_movie('Lion King')
    for movie in movies:
        print(movie.getID())
        print(movie.get('title'))
        print(movie.get('kind'))
        print(movie.get('year'))
        print(movie.items())
        print(movie.get_fullsizeURL())

    specific_movie = ia.get_movie('0110357')
    print(specific_movie)


def get_series():
    series = ia.get_movie('0389564')
    print(series)
    print(series['kind'])
    print(series.get_fullsizeURL())
    # episode = ia.get_movie('0502803')
    # print(episode)
    # print(episode['kind'])
    ia.update(series, 'episodes')
    print(sorted(series['episodes'].keys()))
    season4 = series['episodes'][4]
    print(len(season4))
    episode = series['episodes'][4][2]
    print(episode.getID())

    print(episode['season'])
    print(episode['episode'])
    print(episode['title'])
    print(episode['series title'])
    print(episode['episode of'])
    print(series)

#get_movie()
#get_series()
movie_info_set = ia.get_movie_infoset()
print(movie_info_set)
movie = ia.get_movie('0094226')#, info=['critic reviews', 'plot','release dates', 'release info','vote details','main'])


print(movie)
print(movie.infoset2keys)


print(movie.get('genres'))
print(movie.get('runtimes'))
print(movie.get('rating'))
print(movie.get('votes'))
print(movie.get('imdbID'))
print(movie.get('plot outline'))
print(movie.get('languages'))
print(movie.get('title'))
print(movie.get('year'))
print(movie.get('kind'))
print(movie.get('directors'))
print(movie.get('writers'))
print(movie.get('producers'))
print(movie.get('cast'))
print(movie.get_fullsizeURL())
#       ['genres'])
# runtimes
# rating
# votes
# 'imdbID',\
# 'plot outline', 'languages', 'title', 'year', 'kind', 'directors', 'writers', 'producers', cast
# print(movie.get('title'))
# print(movie.get('plot')[0])
# print(movie.get('plot')[1])
#
# print(movie.get('critic reviews')[0])
#
# print(movie.get('release dates')[1])
#
# print(movie.get('vote details'))
# )

