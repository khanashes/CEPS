from django.urls import path
from .views import deleteWishlist ,HomeView, addToWishList, wishListView, SearchView,filterView, compareView #scraper
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    #path('scrape/', scraper, name="scraper"),
    path('addtowishlist/<int:pk>', addToWishList, name="addToWishList"),
    path('wishlistview/', wishListView, name="wishListView"),
    path('search/', SearchView, name="search"),
    path('filter/<str:query>/', filterView, name="filter"),
    path('compare/<int:id>/', compareView, name="compare"),
    path('deleteWishlist/<int:id>/', deleteWishlist, name="deleteWishlist" ),
]
   