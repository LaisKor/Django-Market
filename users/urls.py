from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, ProfileView, LikedItemsListView, FollowersListView, FollowingListView, follow


app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/liked-items/', LikedItemsListView.as_view(), name='liked_items_list'),
    path('<str:username>/followers/', FollowersListView.as_view(), name='followers_list'),
    path('<str:username>/following/', FollowingListView.as_view(), name='following_list'),
    path('<str:username>/follow/', follow, name='follow'),
]