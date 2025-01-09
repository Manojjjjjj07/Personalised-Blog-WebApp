from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.utils.html import mark_safe
from django.db.models import F, Func, Value, IntegerField
from django.db.models.functions import Cast
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Reaction

def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query) if query else None
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'BlogPop/search_posts.html', context)

def update_reaction(request, post_id, reaction_type):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to react.'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    user = request.user
    existing_reaction = Reaction.objects.filter(post=post, user=user).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
    else:
        Reaction.objects.create(post=post, user=user, reaction_type=reaction_type)

    reaction_count = {
        'likes': Reaction.objects.filter(post=post, reaction_type='like').count(),
        'loves': Reaction.objects.filter(post=post, reaction_type='love').count(),
        'claps': Reaction.objects.filter(post=post, reaction_type='clap').count(),
    }

    return JsonResponse(reaction_count)


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'BlogPop/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'BlogPop/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'BlogPop/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def popular_posts(request):
    posts = Post.objects.annotate(
        likes=Count('reactions', filter=Q(reactions__reaction_type='like')),
        loves=Count('reactions', filter=Q(reactions__reaction_type='love')),
        claps=Count('reactions', filter=Q(reactions__reaction_type='clap')),
    ).annotate(
        popularity=F('likes') + F('loves') + F('claps')  # Calculate popularity
    ).order_by('-popularity')

    return render(request, 'BlogPop/popular_posts.html', {'posts': posts})

def about(request):
    return render(request, 'BlogPop/about.html', {'title': 'About'})
