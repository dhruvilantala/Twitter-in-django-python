from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('profile_list/',views.profile_list, name='profile_list'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('login/',views.login_user, name='login'),
    path('register/',views.register_user, name='register'),
    path('logout/',views.logout_user, name='logout'),
    path('meep_like/<int:pk>',views.meep_like, name='meep_like'),
    path('meep_show/<int:pk>',views.meep_show, name='meep_show'),
    path('update_user/',views.update_user, name='update_user'),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('meep_comment/<int:pk>',views.meep_comment, name='meep_comment'),
    path('follow/<int:pk>', views.follow, name="follow"),
    path("delete_comment/<int:pk>", views.delete_comment , name = "delete_comment" ),
    path("delete_meep/<int:pk>", views.delete_meep , name = "delete_meep" ),
    path("edit_meep/<int:pk>", views.edit_meep , name = "edit_meep" ),
    path("like_comment/<int:pk>", views.like_comment , name = "like_comment" ),
]
