from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse 
from .models import Posts
from .forms import CreatePostsForm, UpdatePostsForm, DeletePostsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here




def home(request):
    context = {
        'posts': Posts.objects.all()
    }
    return render(request, 'blog/home.html', context)



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



@login_required
def create(request):
    if request.method == "POST":
        f = CreatePostsForm(request.POST)
        if f.is_valid():
            submission = f.save(commit=False)
            submission.author = request.user
            submission.save()
            return redirect('home-blog')
    else:
        f = CreatePostsForm()

    return render(request, 'blog/create.html', {"form": f})


@login_required
def update(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Posts, pk=post_id)
        f = UpdatePostsForm(request.POST, instance=post)
        if f.is_valid():
            submission = f.save(commit=False)
            if submission.author == request.user:
                submission.save()
                return redirect('/post/' + str(post_id))    # !!!!**********
            else:
                raise Exception("You can't update this post!")
    else:
        post = get_object_or_404(Posts, pk=post_id)
        f = UpdatePostsForm(instance=post)
    return render(request, 'blog/update.html', {"form": f, "post": post})


@login_required
def delete(request, post_id):
    new_to_delete = get_object_or_404(Posts, id=post_id)
    #+some code to check if this object belongs to the logged in user

    if request.method == 'POST':
        form = DeletePostsForm(request.POST, instance=new_to_delete)

        if form.is_valid(): # checks CSRF
            submission = form.save(commit=False)
            if submission.author == request.user:
                new_to_delete.delete()
                return redirect("home-blog") # wherever to go after deleting
            else:
                raise Exception("You can't delete this post !")

    else:
        form = DeletePostsForm(instance=new_to_delete)

    return render(request, 'blog/delete.html', {'form': form, 'new_to_delete': new_to_delete})



def detail(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    context = {
        'posts': post
    }
    return render(request, 'blog/detail.html', context) 


class UserPostListView(ListView):
    model = Posts
    template_name = "blog/authorpost.html"
    context_object_name = 'posts'
    ordering = ["-date_posted"]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])   # or use self.kwargs.get('username)
        return Posts.objects.filter(author=user).order_by("-date_posted")






# instead of using Function Based Views, we can also use the folllowing  Class Based Views >>>>>>>>>>>>>>>>>>>>...................<<<<<<<<!



class AboutView(TemplateView):
    template_name = "blog/about.html"



class PostListView(ListView):
    model = Posts                                                  # by default ListView uses name "object_list" in the template
    template_name = "blog/home.html"                               # to represent the instances of Model i.e, the list of all the 
    context_object_name = 'posts'                                  # objects(instances) of a database model
    ordering = ["-date_posted"]


# by default DetailView uses name "object" or "the lowercased name of our model" 
# in the template to represent the instances of Model 


class PostDetailView(DetailView):
    model = Posts                          

    # by default CBV looks for a template with naming
    # convention as >>> templates/myapp/modelname_viewtype.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']                        # by default CreateView looks for a template with naming
                                                         # convention >>>> templates/myapp/modelname_form.html
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']                            # UpdateView uses the same template as Createview
                                                             # CreateView and Update View both use the same template
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts                                                                 # by default DeleteView looks for a template with naming
    success_url = "/"                                                             # convention >>>> templates/myapp/modelname_confirm_delete.html

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
