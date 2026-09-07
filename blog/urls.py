from django.urls import path

from . import views


app_name = "blog"


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # BLOG DETAIL
    # =====================================================

    path(
        "blog/<slug:slug>/",
        views.blog_detail,
        name="blog_detail"
    ),


    # =====================================================
    # ABOUT
    # =====================================================

    path(
        "about/",
        views.about,
        name="about"
    ),


    # =====================================================
    # TOPIC
    # =====================================================

    path(
        "topic/<str:topic_name>/",
        views.topic,
        name="topic"
    ),


    # =====================================================
    # SEARCH
    # =====================================================

    path(
        "search/",
        views.search,
        name="search"
    ),


    # =====================================================
    # MY BLOGS
    # =====================================================

    path(
        "my-blogs/",
        views.my_blogs_view,
        name="my_blogs"
    ),


    # =====================================================
    # CREATE BLOG
    # =====================================================

    path(
        "create-blog/",
        views.create_blog_view,
        name="create_blog"
    ),


    # =====================================================
    # LIKE
    # =====================================================

    path(
        "blog/<slug:slug>/like/",
        views.like_blog,
        name="like_blog"
    ),


    # =====================================================
    # SAVE / UNSAVE
    # =====================================================

    path(
        "blog/<slug:slug>/save/",
        views.save_blog,
        name="save_blog"
    ),


    # =====================================================
    # COMMENT
    # =====================================================

    path(
        "blog/<slug:slug>/comment/",
        views.add_comment,
        name="add_comment"
    ),


    # =====================================================
    # DELETE BLOG
    # =====================================================

    path(
        "delete-blog/<int:blog_id>/",
        views.delete_blog_view,
        name="delete_blog"
    ),


    # =====================================================
    # SAVED BLOGS
    # =====================================================

    path(
        "saved-blogs/",
        views.saved_blogs,
        name="saved_blogs"
    ),
    path(
    'contact/',
    views.contact,
    name='contact'
    ),
    path(
    "join-community/",
    views.join_community,
    name="join_community"
),
]