from bs4 import BeautifulSoup
import requests
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})


class Movie:
    def __init__(self, overview, director, writer, stars, country, lang, rating, total_ratings, poster):
        self.overview = overview
        self.director = director
        self.writer = writer
        self.stars = stars
        self.country = country
        self.lang = lang
        self.rating = rating
        self.total_ratings = total_ratings
        self.poster = poster


def scrap(id):
    url = 'https://www.imdb.com/title/' + id
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    overview = str(soup.findAll("div", {"class": "summary_text"})[0])[47:].split('\n')[0]
    try:
        poster = str(soup.findAll('div', {'class': 'poster'})[0].find_all('img')[0]).split('src="')[1].split('" title')[0]
    except:
        poster = 'https://m.media-amazon.com/images/M/MV5BMDQ5OTY5ZDUtM2JlNC00ZjMyLWJhZGQtNTY1ZjY2NDk4ZjRlXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UY268_CR4,0,182,268_AL_.jpg'
    credits = soup.findAll('div', {'class': 'credit_summary_item'})
    director = ''
    writer = ''
    stars = ''
    for item in credits:
        if 'Director' in str(item.find_all('h4')):
            for direct in item.find_all('a'):
                director += str(direct).split('\">')[1][:-4]
                if len(director) > 0 and item.find_all('a').index(direct) != len(item.find_all('a')) - 1:
                    director += ', '
        if 'Writer' in str(item.find_all('h4')):
            for writ in item.find_all('a'):
                writer += str(writ).split('\">')[1][:-4]
                if len(writer) > 0 and item.find_all('a').index(writ) != len(item.find_all('a')) - 1:
                    writer += ', '
        if 'Stars' in str(item.find_all('h4')):
            for star in item.find_all('a'):
                if 'See full cast' in str(star):
                    stars = stars[:-2]
                    break
                stars += str(star).split('\">')[1][:-4]
                if len(stars) > 0 and item.find_all('a').index(star) != len(item.find_all('a')) - 1:
                    stars += ', '

    ratings = soup.findAll('div', {'class': 'ratingValue'})
    try:
        rating = str(ratings[0]).split('">')[1][16:19]
        total_ratings = str(ratings[0]).split('">')[1][29:].split(' user')[0]
    except:
        rating = 'N/A'
        total_ratings = 'N/A'

    details = soup.findAll('div', {'class': 'article', 'id': 'titleDetails'})
    x = details[0].find_all('a')
    country = 'N/A'
    lang = 'N/A'
    for a in x:
        if 'country_of_origin' in str(a):
            country = str(x[x.index(a)]).split('">')[1][:-4]
        if 'primary_language' in str(a):
            lang = str(x[x.index(a)]).split('">')[1][:-4]

    return Movie(overview, director, writer, stars, country, lang, rating, total_ratings, poster)