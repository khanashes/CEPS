from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Product, WishList 
from bs4 import BeautifulSoup
from requests import get
from django.contrib import messages
import lxml
from django.db.models import Q
from notifications.signals import notify
# followings are our views.
#------------------------------------------------------------
#------------------------------------------------------------
# home view
#------------------------------------------------------------
#------------------------------------------------------------
class HomeView(ListView):
    model               = Product
    template_name       = "scraper/home.html"
    context_object_name = "products"
    paginate_by         = 20

"""
#------------------------------------------------------------
#------------------------------------------------------------
# mega Site scraper
#------------------------------------------------------------
#------------------------------------------------------------
def mega():
    pageNumber  = 1
    nextPage    = True
    proList     = []
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

#------------------------------------------------------------
#------------------------------------------------------------
# PakMobiZone.pk scraper
#------------------------------------------------------------
#------------------------------------------------------------

def pakiMobZone():
    url         = 'https://www.pakmobizone.pk/mobile-phone/'
    getRequest  = get(url)
    product     = []
    def scrapeProduct(scrapeData):
        unorderList = scrapeData.find('div', class_="qt-phones-wrapper")
        orderList = unorderList.find_all('div', class_='col-xs-3 col-sm-2')
        returnProduct = []
        for ol in orderList:
            image = ol.find('img')['src']
            productUrl = ol.find('a')['href']
            titlePage = ol.find('h3', class_="qt-phone-thumb-title")
            title = titlePage.find('a').text
            price = ol.find(
                'div', class_="qt-phone-thumb-price").text.replace("Rs.", "").replace("\t", "").replace(',',"")
            if "Not" in price:
                continue
            else:
                price = int(price)
                pro = Product(title=title, price=price, productUrl=productUrl,imageUrl=image, site="pakmobizone.pk")
                returnProduct.append(pro)
        return returnProduct
    scrapeData = BeautifulSoup(getRequest.content, features='lxml')
    unorderList = scrapeData.find(id="taxonomy_term_widget-11")
    orderList = unorderList.find_all('li', class_="cat-item")
    for ol in orderList:
        url = ol.find('a')['href']
        html_content = get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        product = product + scrapeProduct(soup)
    return  product


#------------------------------------------------------------
#------------------------------------------------------------
# myshop.pk scraper
#------------------------------------------------------------
#------------------------------------------------------------

def myShop():
    nextPage = True
    pageNumber = 1
    proList = []
    while nextPage:
        url = 'https://myshop.pk/mobiles-smartphones-tablets/smartphones?p={}'.format(
            pageNumber)
        response = get(url).text
        soup = BeautifulSoup(response, features='lxml')
        nextPage = soup.find('li', class_="item pages-item-next")
        if not nextPage:
            nextPage = False
        li = soup.find_all('li', class_='item product product-item')
        for item in li:
            titlePage = item.find("strong", class_='product name product-item-name')
            title = title = titlePage.find('a').text.replace(" ","").replace(":","").replace("1y","").replace("("," ").replace(")"," ").replace("|"," ").replace("-"," ")
            productUrl = titlePage.find('a')['href']
            image = item.find('img')['src']
            price = item.find('span', class_='price').text.split(".")[0]
            price = int(price.replace("Rs","").replace(",","").replace(" ",""))
            pro = Product(title=title, price=price, productUrl=productUrl,imageUrl=image, site="myshop.pk")
            proList.append(pro)
        pageNumber = pageNumber + 1
    return proList

#------------------------------------------------------------
#------------------------------------------------------------
# Yavo Site scraper
#------------------------------------------------------------
#------------------------------------------------------------
def yavo():
    product = []
    nextPage = True
    pageNumber = 1
    while nextPage:
        url = 'http://yayvo.com/mobiles-tablets/smartphones.html?p={}'.format(
            pageNumber)
        response = get(url).text
        soup = BeautifulSoup(response, features='lxml')
        if not soup.find('a', class_="next i-next"):
            nextPage = False
        data = soup.find("div", class_='category-products')
        ul = data.find_all('ul', 'products-grid')
        for unorderList in ul:
            li = unorderList.find_all('li', class_="item")
            for listData in li:
                titlePage = listData.find('h2', class_="product-name")
                title = titlePage.find('a').text
                price = int(listData.find('span', class_="price").text.replace(
                    " ", "").replace("\n", "").replace('Rs.',"").replace(",",""))
                productUrl = listData.find("a")['href']
                image = listData.find("img", class_="b-lazy")['data-src']
                pro = Product(title=title, price=price, productUrl=productUrl,imageUrl=image, site="yavo.pk")
                product.append(pro)
        pageNumber = pageNumber + 1
    return product

#------------------------------------------------------------
#------------------------------------------------------------
# Scraper function just for testing
#------------------------------------------------------------
#------------------------------------------------------------

def scraper(request):
    products = pakiMobZone() + mega() + yavo() + myShop()
    print("hello")
    for product in products:
        find = Product.objects.filter(title=product.title, productUrl = product.productUrl)
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
                        verb = "Price is updated from {} to {}".format(x.price, product.price)
                        notify.send(wishlist, recipient=wishlist.user, verb=verb)
    return redirect('home')"""
#------------------------------------------------------------
#------------------------------------------------------------
# Add to wishlist
#------------------------------------------------------------
#------------------------------------------------------------
@login_required(login_url='login') 
def addToWishList(request,pk):
    product = get_object_or_404(Product,pk=pk)
    check = WishList.objects.filter(user = request.user, product= product)
    if not check:
        wishlist = WishList(user = request.user, product=product)
        wishlist.save()
        return redirect('home')
    else:
        messages.error("Already present in your wishlist")
        return redirect('home')

#------------------------------------------------------------
#------------------------------------------------------------
# Wishlist View
#------------------------------------------------------------
#------------------------------------------------------------

@login_required(login_url='login') 
def wishListView(request):
    products = request.user.wishlist_set.all()
    return render(request, 'scraper/wishlist.html', context={'products':products})


#------------------------------------------------------------
#------------------------------------------------------------
# Search View
#------------------------------------------------------------
#------------------------------------------------------------
def SearchView(request):
    if request.method == "GET":
        query = request.GET.get('query')
        products = Product.objects.filter(Q(title__icontains=query) | Q(productUrl__icontains=query)).order_by("-price")
        return render(request, "scraper/search.html",context={"products":products, "query":query})


#------------------------------------------------------------
#------------------------------------------------------------
# Filter View
#------------------------------------------------------------
#------------------------------------------------------------

def filterView(request,query):
    if request.method == 'GET':
        mini = request.GET.get('Min')
        maxi = request.GET.get('Max')
        productList = Product.objects.filter(Q(title__icontains=query) | Q(productUrl__icontains=query))
        products = []
        for prod in productList:
            if prod.price >= int(mini) and prod.price <= int(maxi):
                products.append(prod)
        return render(request, "scraper/search.html",context={"products":products, "query":query,"minimum":mini,"maximum":maxi})


#------------------------------------------------------------
#------------------------------------------------------------
# Compare View
#------------------------------------------------------------
#------------------------------------------------------------

def compareView(request, id):
    product = Product.objects.get(id=id)
    proStr = product.title.split(" ") 
    productList = []
    products = []
    length = len(proStr)
    if length < 2:
        productList = Product.objects.filter(Q(title__icontains=proStr[0]) | Q(productUrl__icontains=proStr[0])).filter(Q(title__icontains=proStr[1]) | Q(productUrl__icontains=proStr[1]))
    elif length > 2:
        productList = Product.objects.filter(Q(title__icontains=proStr[0]) | Q(productUrl__icontains=proStr[0])).filter(Q(title__icontains=proStr[1]) | Q(productUrl__icontains=proStr[1])).filter(Q(title__icontains=proStr[2]) | Q(productUrl__icontains=proStr[2]))
   
    
    minimum = product.price
    maximum = product.price
    average = product.price
    for pro in productList:
        if pro.price < minimum:
            minimum = pro.price
        if pro.price > maximum:
            maximum = pro.price
    average = (minimum+maximum)/2
    for pro in productList:
        if pro.title != product.title:
            products.append(pro)
        
    closeMatches = len(products)
    context = {
        "product":product,
        "products":products,
        "minimum":minimum,
        "maximum":maximum,
        "average":average,
        "closeMatches":closeMatches,
    }
    return render(request, template_name="scraper/compare.html", context=context)

#------------------------------------------------------------
#------------------------------------------------------------
# delete wishlist View
#------------------------------------------------------------
#------------------------------------------------------------

@login_required(login_url='login') 
def deleteWishlist(request, id):
    wishlist = WishList.objects.get(id=id)
    wishlist.delete()
    return redirect("wishListView")