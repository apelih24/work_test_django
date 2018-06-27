from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import generic
from .models import Post


class IndexView(generic.ListView):
    template_name = 'SocialNetwork/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:5]


class PostInfoView(generic.DetailView):
    model = Post
    template_name = 'SocialNetwork/post_info.html'

# def post_info(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     context = {'post': post}
#     return render(request, 'SocialNetwork/post_info.html', context)
