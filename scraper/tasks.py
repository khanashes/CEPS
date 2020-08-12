from celery import task
from .models import Product, WishList
from celery import shared_task
from bs4 import BeautifulSoup
from requests import get
import lxml
from notifications.signals import notify
def mega():
    pageNumber = 1
    nextPage = True
    proList = []
    while nextPage:
        url = "http://www.mega.pk/mobiles/{}/".format(pageNumber)
        response = get(url)
        soup = BeautifulSoup(response.text, features="lxml")
        ul = soup.find('ul', class_='item_grid list-inline clearfix')
        li = ul.find_all('li', class_='col-xs-6')
        if not li:
            break
        for link in li:
            if link.find("div", class_="was"):
                title = link.find(id="lap_name_div").text.replace("\n", "")
                data = link.find("div", class_="cat_price").text.replace(
                    "\n", "").replace("\t", "").replace(" ", "")
                lists = data.split("-")
                if len(lists) > 2:
                    price = lists[1].replace("PKR", "") + "-PKR"
                else:
                    price = data
                price = int(price.replace(",", "").replace(
                    '-', "").replace("PKR", ""))
                productUrl = link.find("a")['href']
                image = link.find("img")['data-original']
                pro = Product(title=title, price=price, productUrl=productUrl,imageUrl=image, site="mega.pk")
                proList.append(pro)    
        pageNumber = pageNumber + 1
    return proList


@shared_task
def scrape_data(self):
    products = mega()
    for product in products:
        find = Product.objects.filter(title=product.title)
        if not find:
            pro = Product(title=product.title,price=product.price,productUrl=product.productUrl,imageUrl=product.imageUrl,site=product.site)
            pro.save()
        if find:
            if find[0].price != product.price:
                Product.objects.filter(title=product.title).update(price=product.price)
                x = find[0]
                w = WishList.objects.filter(product=x)
                if w:
                    for wishlist in w:
                        notify.send(wishlist, recipient=wishlist.user, verb='you reached level 10')
                        print('change')
                        """notify = Notification(user = wishlist.user, changeMessage="Price is updated from {} to {}".format(x.price, product.price))
                        notify.save()"""
                        