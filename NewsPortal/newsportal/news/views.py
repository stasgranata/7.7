from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from .models import Author, Post, Category, Comment, PostCategory
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-creationDate'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 20


class SearchList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'firstnews.html'
    context_object_name = 'firstnews'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        if 'articles' in self.request.path:
            post = form.save(commit=False)
            post.is_article = True
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if ('news' in self.request.path) and post.is_article:
            raise ValidationError(
                "Вы пытаетесь редактировать статью как новость."
            )
        elif ('articles' in self.request.path) and not post.is_article:
            raise ValidationError(
                "Вы пытаетесь редактировать новость как статью."
            )
        else:
            return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

