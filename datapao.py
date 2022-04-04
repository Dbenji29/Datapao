import requests
from bs4 import BeautifulSoup
import re

#Returns a list of (movie title, rating, number of ratings, number of Oscars)
def Scraper():
    html = requests.get('https://www.imdb.com/chart/top/').text
    soup = BeautifulSoup(html, 'lxml')
    
    movies = soup.select('td.titleColumn a')[:20]
    #Top 20 movie titles in a list
    titles = [i.text for i in movies]
    
    numbers = soup.select('td.imdbRating strong')[:20]
    #Rating values list
    ratings = []
    #Number of ratings list
    raters = []
    for i in numbers:
        j = i['title']
        ratings.append(j[:3])
        raters.append(re.search('on (.*) user', j).group(1))
    
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
    
    return list(zip(titles, ratings, raters, oscars))

def ReviewPenalizer():

def OscarCalculator():