import requests
import datetime
from bs4 import BeautifulSoup
import random
from datetime import datetime
import json

#Sometimes picking a movie is hard

def clock():
    current = datetime.now()
    clock_format = current.strftime('%Y/%m/%d %I:%M:%S:%f')
    return str(clock_format) + " CST"


print(clock(), ':: I am here to help you choose a movie')


class Movie():
    def __init__(self):
        self.session = requests.session()
        self.headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.movie_selection = []

    def movie_list(self):
        #Adjust the numbers here to loop through more pages
        for page in range(1,15):
            self.movie_page = self.session.get('https://letterboxd.com/films/ajax/popular/this/month/size/small/page/'+
            str(page), headers=self.headers)
            self.soup = BeautifulSoup(self.movie_page.text,'html.parser')
            self.table = self.soup.find_all('li', {'class': 'listitem poster-container'})
            # Loops through movie list and appends to list
            for results in self.table:
                self.title = results.find('div')('a')[0]['title']
                self.movie_selection.append(self.title)
        print(clock(), ':: Choosing from', len(self.movie_selection), 'movies')
        print(clock(), ':: Selecting a movie')
        self.rando_movie = random.choice(self.movie_selection)
        # The Lion King
        self.movie_name = self.rando_movie[:-6].strip()
        # Makes movie lowercase for better matches
        self.movie_lower = self.movie_name.lower()
        print(clock(), ':: The movie chosen is', self.rando_movie)
        self.movie_year = self.rando_movie[-5:-1]
        # Formatted to be able to search RT
        self.name = self.movie_name.replace(' ', '_')
        self.name_title = self.name.replace('_', '%20')


    #Goes to Rotten Tomatoes to get rating
    def movie_review(self):
        self.rotten_tom = self.session.get('https://www.rottentomatoes.com/search?search=' + str(self.name_title),
        headers=self.headers)
        #print(rotten_tom.url)
        self.tea = BeautifulSoup(self.rotten_tom.text, 'html.parser')
        self.table = self.tea.find_all('script', attrs={'type': 'application/json'})[1]
        for info in self.table:
            #Easier to parse this way
            self.info = json.loads(info)
            self.doc = self.info['items']
            for x in self.doc:
                self.mov = x['name'].lower()
                #searches for matches
                if self.mov == self.movie_lower and self.movie_year == x['releaseYear']:
                    self.tomato = x['tomatometerScore']['score']
                    self.aud = x['audienceScore']['score']
                    print(clock(), ':: FOUND MOVIE ON ROTTEN TOMATOES')
                    print(clock(), '::', x['name'], 'ranked in at', self.tomato, 'on the TOMATOMETER with an AUDIENCE SCORE of',
                    self.aud)


ex = Movie()
ex.movie_list()
ex.movie_review()
