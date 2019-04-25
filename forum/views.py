from django.shortcuts import render

# Create your views here.


def forum_home(request):

    return render(request, 'forum/forum_home.html')


def forum_create(request):

    return render(request, 'forum/forum_create.html')


def forum_feed(request):

    return render(request, 'forum/forum_feed.html')


def forum_search(request):

    return render(request, 'forum/forum_search.html')