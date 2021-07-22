# Edworthy
## A web scraping project that tells me when and where to go on walks

## Tech
This is a discord bot written in python.
It uses discord.py to run the bot, and uses BeautifulSoup to collect data on different parks that I can go for walks at.
The code can be found at [main.py](https://github.com/dungwoong/edworthy/blob/master/main.py)

I'm trying to adapt it to get data for locations other than parks, which is why I put in Damascus Calgary(good place to eat btw) as a test.

## Premise
I live in Calgary, Alberta. I like going on walks to Edworthy Park. However, I want to go when there are few people there, because of Covid.<br>
Google collects data on the "popularity" of locations such as Edworthy, which you can see in page.html. However, the stats given is probably an average across all seasons, and true is usually different in the summer(as school is out, it's nice outside, etc.)<br>
I want to know when Edworthy(or any of the other parks in Calgary that are close to me) has few people in it.<br>

Google API doesn't give popularity info, and api calls cost money. Therefore, I will simply scrape the search results page that can be found in the HTML in this repository.

## Usage.
I don't know why you would want to use this, but here's how:<br>
 - Get a discord token, make a config.json and put it in with the key of "token"
 - Put in some location names
 - Run main.py. This is a discord bot, so you have to invite it to a server. Type ?help for help.
 - ?park gives you park info. 100 is maximum occupancy, 0 is minimum. It tells you the ratio of current occupancy to usual(average) occupancy, as well as the value of current occupancy, for each location.
 
 ## How does it work?
 Download [page.html](https://github.com/dungwoong/edworthy/blob/master/page.html) and load it. Google doesn't give specific popularity data, but it gives a visual that is made out of a bunch of divs.
 Using BeautifulSoup, I get the height of these divs, and we can report on "approximate" data. I don't need specific numbers anyways.
