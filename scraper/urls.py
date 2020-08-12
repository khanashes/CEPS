from django.urls import path
from .views import HomeView, addToWishList, wishListView,scraper, SearchView,filterView
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('scrape/', scraper, name="scraper"),
    path('addtowishlist/<int:pk>', addToWishList, name="addToWishList"),
    path('wishlistview/', wishListView, name="wishListView"),
    path('search/', SearchView, name="search"),
    path('filter/<str:query>/', filterView, name="filter")
]
