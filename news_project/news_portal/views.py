from django.shortcuts import render
from django.views import View
# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, PostUpdate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



# Create your views here.

'''
class PostList(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
'''

'''
class PostList(View):
    def get(self, request):
        posts = Post.objects.order_by('-id')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page',1))
        data = {'posts':posts}
        return render(request,'post.html',data)
'''


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news_portal/post.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news_portal/post_detail.html'
    context_object_name = 'post_detail'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)
    template_name = 'news_portal/create_post.html'
    form_class = PostForm
    success_url = '/'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post',)
    template_name = 'news_portal/delete_post.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()
    success_url = '/'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post',)
    template_name = 'news_portal/update_post.html'
    form_class = PostUpdate
    success_url = '/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk = id)


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

