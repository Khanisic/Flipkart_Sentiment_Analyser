import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from string import punctuation
from nltk.corpus import stopwords

nltk.download('stopwords')

BASE_URL = 'https://www.flipkart.com/search?q={}'
CLEANR = re.compile('<.*?>')

# Create your views here.
def home(request):
    return render(request, 'base.html')

def gadgets(request):
    return render(request, 'my_app/gadgets.html')

def clothing(request):
    return render(request, 'my_app/clothing.html')

def other(request):
    if(request.POST.get('search')):
        search = request.POST.get('search')
        final_url = BASE_URL.format(quote_plus(search))
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')

        product_data = soup.find_all('div', {'class': '_4ddWXP'})

        final_postings = []
        product_links = []
        stop_words = stopwords.words('english')
        sa = SentimentIntensityAnalyzer()

        for post in product_data[0:4]:
            product_titles = post.find('a', {'class': 's1Q9rs'}).text
            product_img = post.find('img', {'class': '_396cs4 _3exPp9'}).get('src')
            product_link = "https://flipkart.com" + post.find('a', {'class': '_2rpwqI'}).get('href')
            if post.find('div', {'class': '_3LWZlK'}):
                if post.find('div', {'class': '_3LWZlK'}).text:
                    product_star = post.find('div', {'class': '_3LWZlK'}).text
            else:
                product_star = 'N/A'
            product_price = post.find('div', {"class": '_30jeq3'}).text
            if post.find('span', {'class': '_2_R_DZ'}):
                product_bought = post.find('span', {'class': '_2_R_DZ'}).text
            else:
                product_bought = 'N/A'
            reviewsLink = product_link.replace("/p/", "/product-reviews/")
            product_links.append(reviewsLink)
            final_postings.append((product_titles, product_img, product_link, product_star, product_price[1:], product_bought))

        product_reviews_main = []
        product_review = []
        product_scores = []
        for reviewpage in product_links:
            r = requests.get(reviewpage)
            rdata = r.text
            soup = BeautifulSoup(rdata, features='html.parser')
            reviews = soup.find_all('div', {'class': 't-ZTKy'})
            product_reviews_main.append(re.sub(CLEANR, '', str(reviews)))

        for review in product_reviews_main:
            x = review.split("READ MORE")
            product_review.append(x)

        for i in range(len(product_review)):
            sumcomp = 0
            sumpos = 0
            sumneg = 0
            sumneu = 0
            for j in range(len(product_review[i])):
                ptext = product_review[i][j]
                dd = sa.polarity_scores(ptext)
                compounddd = round((1 + dd['compound']) / 2, 2)
                posdd = dd['pos']
                negdd = dd['neg']
                neudd = dd['neu']
                sumcomp = sumcomp + compounddd
                sumpos = sumpos + posdd
                sumneg = sumneg + negdd
                sumneu = sumneu + neudd
            product_scores.append((round(sumcomp / len(product_review[i]) * 100),round(sumpos / len(product_review[i]) * 100),round(sumneg / len(product_review[i]) * 100),round(sumneu / len(product_review[i]) * 100)))

        print(product_scores)
        front = zip(final_postings, product_scores)
        stuff_for_frontend = {
            'search': search,
            'final_postings': front,
        }
        return render(request, 'my_app/other.html', stuff_for_frontend)
    else:
        return render(request, 'my_app/other.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    product_data = soup.find_all('div', {'class':'_4ddWXP'})

    final_postings = []
    product_links = []
    stop_words = stopwords.words('english')
    sa = SentimentIntensityAnalyzer()

    for post in product_data[0:1] :
        product_titles = post.find('a', {'class': 's1Q9rs'}).text
        product_img = post.find('img', {'class': '_396cs4 _3exPp9'}).get('src')
        product_link = "https://flipkart.com"+post.find('a', {'class': '_2rpwqI'}).get('href')
        if post.find('div', {'class': '_3LWZlK'}):
            if post.find('div', {'class': '_3LWZlK'}).text:
                product_star = post.find('div', {'class': '_3LWZlK'}).text
        else:
            product_star = 'N/A'
        product_price = post.find('div', {"class": '_30jeq3'}).text
        if post.find('span', {'class': '_2_R_DZ'}):
            product_bought = post.find('span', {'class': '_2_R_DZ'}).text
        else:
            product_bought = 'N/A'
        reviewsLink = product_link.replace("/p/", "/product-reviews/")
        product_links.append(reviewsLink)
        final_postings.append((product_titles,product_img,product_link,product_star,product_price,product_bought))



    product_reviews_main = []
    product_review = []
    product_scores = []
    for reviewpage in product_links:
        r = requests.get(reviewpage)
        rdata = r.text
        soup = BeautifulSoup(rdata, features='html.parser')
        reviews = soup.find_all('div', {'class':'t-ZTKy'})
        product_reviews_main.append(re.sub(CLEANR,'',str(reviews)))

    for review in product_reviews_main:
        x = review.split("READ MORE")
        product_review.append(x)

    for i in range(len(product_review)):
        sum = 0
        for j in range(len(product_review[i])):
            text = product_review[i][j]
            text_final = ''.join(c for c in text if not c.isdigit())
            processed_review = ' '.join([word for word in text_final.split() if word not in stop_words])
            dd = sa.polarity_scores(text=processed_review)
            compound = round((1 + dd['compound']) / 2, 2)
            sum = sum + compound
        product_scores.append(round(sum/len(product_review[i]) * 100))

    print(product_scores)
    front = zip(final_postings,product_scores)
    stuff_for_frontend = {
        'search': search,
        'final_postings': front,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)