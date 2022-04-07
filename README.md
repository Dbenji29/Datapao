# Datapao interview assignment
Link:
https://datapao.notion.site/The-Big-IMDB-quest-54dae47fbe8b4e97b87dc60379f5c28d

How to run: Just run the script and the results will be in results.csv file.

# The Big IMDB quest

## Objective
Your assignment is to create an application that scrapes data from [IMDB](https://www.imdb.com/chart/top/) and adjusts IMDB ratings based on some rules. You don’t have to extract the whole list, please concentrate your attention on the TOP 20 movies only.

## Tasks
- Implement assignment using:
  - Language: **any language**
  - Libraries: **any libraries**
- Three functions are required:
  - Scraper - See below
  - Rating Adjustment
    - Oscar Calculator - See Below
    - Review Penalizer - See Below
  - Provide Unit tests for all functions
- Write out the TOP 20 movies in a sorted (descending) way including both the original and the adjusted new ratings to a file (JSON, CSV, txt, etc..).
- Provide detailed instructions on how to run your assignment in a separate markdown file.

## Scraper
Scrape the following properties for each movie from the [IMDB TOP 250](https://www.imdb.com/chart/top/) list. It is part of the exercise to design the data structure for it: 
- Rating
- Number of ratings
- Number of Oscars
- Title of the movie

## Review Penalizer:
Ratings are good because they give us an impression of how many people think a film is good or bad. However, it does matter how many people voted. The goal of this exercise is to penalize those films where the number of reviews is low. 

Find the film with the maximum number of reviews (remember, out of the TOP 20 only). This is going to be the benchmark. Compare every movie’s number of reviews to this and penalize each of them based on the following rule: Every 100k deviation from the maximum translates to a point deduction of 0.1. 

*For example*, suppose the maximum number of reviews is 2.456.123. For a given movie with 1.258.369 ratings and an IMDB score of 9.4, the amount of the deduction is 1.1 and therefore the adjusted rating is 8.3.

## Oscar Calculator
The Oscars should mean something, shouldn’t they? Here are the rewards for them:
- 1 or 2 oscars → 0.3 point
- 3 or 5 oscars → 0.5 point
- 6 - 10 oscars → 1 point
- 10+ oscars → 1.5 point

*For example*, if a movie is awarded 4 Oscar titles and the original IMDB rating is 7.5, the adjusted value will increase to 8 points.
