from django.urls import path
from .views import home, detail, posts, create_post,search_result, about_site, create_id, id
        
urlpatterns = [
    path("", home, name="home"),
    path("detail/<slug>/", detail, name="detail"),
    path("posts/<slug>/", posts, name="posts"),
    path("create_post/", create_post, name="create_post"),
    path("search_result/", search_result, name="search_result"),
    path("about_site/", about_site, name="about_site"),
    path("create_id/", create_id, name="create_id"),
    path("id/", id, name="id"),


]