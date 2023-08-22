from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'post_list.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        return context


