from django.shortcuts import render

posts = [
    {
        'Author': 'SKM',
        'Title': 'Blog Post 1',
        'Content': 'First post content',
        'Date_Posted': 'November 30, 2024'
    },
    {
        'Author': 'Suz',
        'Title': 'Blog Post 2',
        'Content': 'Second post content',
        'Date_Posted': 'November 30, 2024'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'BlogPop/home.html', context)

def about(request):
    return render(request, 'BlogPop/about.html',  {'title':'About'})