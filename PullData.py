from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import time
import csv, json

url = 'https://play.google.com/store/movies/details/Spider_Man_Far_from_Home?id=8p6PsoccZog&hl=en_US&showAllReviews=true'

# Open Selenium driver
driver_location = '/Users/riaz_hussain/Downloads/chromedriver'
driver = webdriver.Chrome(driver_location)
driver.get(url)

#Remove old file
try:
    os.remove('spiderman.csv')
    os.remove('spidermanlines.csv')
    os.remove('spidermanfinal.csv')
except:
    print('File not found')
print('files deleted')

loop = 0
uid = 0

while loop < 30:

        # Selenium scroll variables
        last_height = driver.execute_script("return document.body.scrollHeight")
        SCROLL_PAUSE_TIME = 1.5
        res = driver.execute_script('return document.documentElement.outerHTML')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        try:
            btn = driver.find_element_by_xpath('/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[3]/div/span/span')
            btn.click()
            print('Show more click #' + loop)
        except:
            print('invalid selector')
        print('Loop # ' + str(loop))
        loop += 1

soup = BeautifulSoup(res, 'lxml')

box = soup.find('div', {'class': 'W4P4ne'})

# ratings
ratings = box.find_all('div', {'class': 'pf5lIe'})

# reviews
reviews = box.find_all('div', {'class': 'UD7Dzf'})

print('Finding Review/Rating Section...')
review_section = soup.find('div', {'class': 'W4P4ne'})
print (len(review_section))


print('Splitting Up Review/Rating...')
entries = review_section.find_all('div', {'class': 'zc7KVe'})
print(len(entries))
print('Outputting Review Data (If Found)...')

print('Writing header line')
with open('spiderman.csv', 'a') as f:
    f.write('UID' + '|' + 'Rating' + '|' + 'Review' + '\n')

if (entries):

    for element in entries:
        uid += 1
        rating = element.find('div', {'class': 'pf5lIe'}).div['aria-label']
        review = element.find('div', {'class': 'UD7Dzf'}).text if element.find('div', {'class': 'UD7Dzf'}) is not None else 'Onomatopoeia'

        with open ('spiderman.csv', 'a') as f:
            f.write(str(uid) + '|' + rating + '|' + review + '\n')



driver.quit()

#Remove duplicate lines containing no review
bad_words = ['Onomatopoeia']

with open('spiderman.csv') as oldfile, open('spidermanlines.csv', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)
print('Removed duplicate rows')

#Convert ratings from string to int
text = open('spidermanlines.csv', 'r')
text = ''.join([i for i in text]) \
    .replace('Rated 1 stars out of five stars|', '1|') \
    .replace('Rated 2 stars out of five stars|', '2|') \
    .replace('Rated 3 stars out of five stars|', '3|') \
    .replace('Rated 4 stars out of five stars|', '4|') \
    .replace('Rated 5 stars out of five stars|', '5|')
x = open("spidermanfinal.csv","w")
x.writelines(text)
x.close()
print('Converted ratings')
