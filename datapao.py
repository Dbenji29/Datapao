import requests
from bs4 import BeautifulSoup
import re
import csv
import unittest

#Database of movies: 4 lists
#Normally I use SQLite, but since this is a small asssignment I won't bother with that :)
class MoviesDB:
    def __init__(self, titles, ratings, raters, oscars):
        self.titles = titles
        self.ratings = ratings
        self.raters = raters
        self.oscars = oscars

#Returns a list of (movie title, rating, number of ratings, number of Oscars)
def Scraper():
    html = requests.get('https://www.imdb.com/chart/top/').text
    soup = BeautifulSoup(html, 'lxml')
    
    movies = soup.select('td.titleColumn a')[:20]
    #Top 20 movie titles in a list
    titles = [i.text for i in movies]
    
    #This is a list of strings like: "<strong title="9.2 based on 2,570,026 user ratings">9.2</strong>"
    numbers = soup.select('td.imdbRating strong')[:20]
    #Rating values list
    ratings = []
    #Number of ratings list
    raters = []
    for i in numbers:
        ratings.append(float(i.text))
        raters.append(int(re.search('on (.*) user', i['title']).group(1).replace(',','')))
    
    #Number of Oscars won (no nominations) list
    oscars = []
    for i in movies:
        html = requests.get('https://www.imdb.com' + i['href'] + 'awards').text
        soup = BeautifulSoup(html, 'lxml')
        #Assuming "Academy Awards, USA" is first in alphabetic order
        award = soup.select('table.awards')[0]
        if(award.select('td.title_award_outcome')[0].text == '\nWinner\nOscar\n'):
            oscars.append(len(award.select('td.award_description')))
        else:
            oscars.append(0)
    
    return MoviesDB(titles, ratings, raters, oscars)

def ReviewPenalizer(ratings, raters):
    m = max(raters)
    return [(i*10 - int((m-j)/100000))/10 for i, j in zip(ratings, raters)]

def OscarCalculator(ratings, oscars):
    def calc(oscars):
        if(oscars > 10):
            return 1.5
        elif(oscars > 5):
            return 1
        elif(oscars > 2):
            return 0.5
        elif(oscars > 0):
            return 0.3
        return 0
    
    return [i+calc(j) for i, j in zip(ratings, oscars)]

data = Scraper()
ratings2 = ReviewPenalizer(data.ratings, data.raters)
ratings2 = OscarCalculator(ratings2, data.oscars)

data2 = list(zip(ratings2, data.titles, data.ratings, data.raters, data.oscars))
data2.sort(key=lambda i: i[0], reverse=True)
with open('results.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(["Adjusted rating", "Title", "Rating", "Number of ratings", "Number of Oscars won"])
    w.writerows(data2)

#%%
class Test(unittest.TestCase):
    def test_Scraper(self):
        self.assertEqual(len(data.titles), 20)
        self.assertIsInstance(data.ratings[19], float)
        self.assertIsInstance(data.raters[19], int)
        self.assertEqual(len(data.oscars), 20)
    
    def test_ReviewPenalizer(self):
        self.assertEqual(ReviewPenalizer([10], [100]), [10])
        self.assertEqual(ReviewPenalizer([10, 10], [100, 100099]), [10, 10])
        self.assertEqual(ReviewPenalizer([10, 10, 10], [100, 100100, 200100]), [9.8, 9.9, 10])

    def test_OscarCalculator(self):
        self.assertEqual(OscarCalculator([0, 0, 0, 0, 0], [0, 2, 4, 8, 16]), [0, 0.3, 0.5, 1, 1.5])

unittest.main()