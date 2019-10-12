from django.shortcuts import render
import requests
from .models import Search
from requests.compat import quote_plus
from bs4 import BeautifulSoup
# Create your views here.
BASE_CRAIG_LIST_URL='https://kenya.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(Search=search)
    final_url = BASE_CRAIG_LIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data, features='html.parser')
    post_listings=soup.find_all('li',{'class':'result-row'})
    # post_titles = post_listings[0].find(class_ ='result-title').text
    # post_url=post_listings[0].find('a').get('href')
    # post_price=post_listings[0].find(class_ ='result-price').text
    # print(post_titles)
    # print(post_url)
    # print(post_price)

    final_postings = []
    for post in post_listings:
        post_titles = post.find(class_ ='result-title').text
        post_url=post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price=post.find(class_ ='result-price').text
        else:
            post_price='N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image=BASE_IMAGE_URL.format(post_image)
            print(post_image)
        else:
            post_image='https://images.craigslist.org/images/peace.jpg'
        final_postings.append((post_titles,post_url,post_price,post_image))


    context = {
        "search":search,
        "final_postings":final_postings,
    }
    return render(request, 'my_app/new_search.html', context)