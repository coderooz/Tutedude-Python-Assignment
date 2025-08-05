from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer
from .forms import BlogPostForm

# REST API View
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer

# UI Views
def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})


def create_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})

