from django.urls import path
from .views import HomeView, scraper, addToWishList, wishListView
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('scrape/', scraper, name="scraper"),
    path('addtowishlist/<int:pk>', addToWishList, name="addToWishList"),
    path('wishlistview/', wishListView, name="wishListView"),

]
