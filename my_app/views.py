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
        positive_words = []
        negative_words = []
        numberofreviews = []

        for reviewpage in product_links:
            r = requests.get(reviewpage)
            rdata = r.text
            soup = BeautifulSoup(rdata, features='html.parser')
            reviews = soup.find_all('div', {'class': 't-ZTKy'})
            noofreviewsuncleaned = soup.find('span', {'class': '_2_R_DZ'})
            noofreviewscleaned = re.sub(CLEANR, '', str(noofreviewsuncleaned))
            noofreviewssplit = noofreviewscleaned.split(';')
            if(noofreviewssplit != ['None']):
                print(noofreviewssplit)
                number = noofreviewssplit[1]
                numbersplit = number.split(' ')
                numberofreviews.append(numbersplit[0])
            else:
                numberofreviews.append(" N/A")
            product_reviews_main.append(re.sub(CLEANR, '', str(reviews)))

        for review in product_reviews_main:
            x = review.split("READ MORE")
            product_review.append(x)

        for i in range(len(product_review)):
            sumcomp = 0
            sumpos = 0
            sumneg = 0
            sumneu = 0

            positive = []
            negative = []

            for review in product_review[i]:
                text1 = review.lower()
                text2 = ''.join(c for c in text1 if not c.isdigit())
                text3 = ''.join(c for c in text2 if c not in punctuation)
                processed_doc1 = ' '.join([word for word in text3.split() if word not in stop_words])
                sa = SentimentIntensityAnalyzer()
                dd = sa.polarity_scores(text1)
                compound = round((1 + dd['compound']) / 2, 2)

                toSplitWords = processed_doc1.split(" ")
                for word in toSplitWords:
                    wd = sa.polarity_scores(word)
                    cd = round((1 + wd['compound']) / 2, 2)

                    if (compound < 0.5):
                        if (cd < 0.5 and cd != 0.5):
                            negative.append(word)
                        if (cd > 0.5 and cd != 0.5):
                            negative.append("Not " + word)
                    if (compound > 0.5):
                        if (cd < 0.5 and cd != 0.5):
                            positive.append("Not " + word)
                        if (cd > 0.5 and cd != 0.5):
                            positive.append(word)

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

            positivefd = nltk.FreqDist(positive)
            negativefd = nltk.FreqDist(negative)

            positivecommon = positivefd.most_common(3)
            negativecommon = negativefd.most_common(3)

            positive_words.append(positivecommon)
            negative_words.append(negativecommon)


        front = zip(final_postings, product_scores, positive_words, negative_words, numberofreviews)
        stuff_for_frontend = {
            'search': search,
            'final_postings': front,
        }
        return render(request, 'my_app/other.html', stuff_for_frontend)
    else:
        return render(request, 'my_app/other.html')

