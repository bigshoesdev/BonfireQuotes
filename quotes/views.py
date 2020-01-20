from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Post, PostForm, Author, Category, Background, Like
from potd.models import PhotoOfTheDay
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect
from marketing.forms import HomeEmailSignupForm


def home(request):
    form = HomeEmailSignupForm()
    context = {
        'post': Post.objects.filter(feature_qotd=True).order_by("-feature_qotd").first(),
        'photo': PhotoOfTheDay.objects.filter(feature_potd=True).order_by("-date_posted").first(),
        'form': form
    }
    return render(request, 'quotes/home.html', context)


def quotes_day(request):
    context = {
        'post': Post.objects.filter(feature_qotd=True).order_by("-feature_qotd").first()
    }
    return render(request, 'quotes/quote_day.html', context)


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['quote', 'author', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            author, created = Author.objects.get_or_create(
                name=form.cleaned_data['author'],
                defaults={'slug': slugify(form.cleaned_data['author'], allow_unicode=True)})

            post = Post(author=author, quote=form.cleaned_data['quote'],
                        slug=slugify(form.cleaned_data['quote'], allow_unicode=True), user=request.user)
            post.save()

            background1, created = Background.objects.get_or_create(
                color=form.cleaned_data['background1'],
                defaults={'slug': slugify(form.cleaned_data['background1'], allow_unicode=True)})

            post.backgrounds.add(background1)

            background2, created = Background.objects.get_or_create(
                color=form.cleaned_data['background2'],
                defaults={'slug': slugify(form.cleaned_data['background2'], allow_unicode=True)})

            post.backgrounds.add(background2)

            if form.cleaned_data['category1'] != "":
                category1, created = Category.objects.get_or_create(
                    name=form.cleaned_data['category1'],
                    defaults={'slug': slugify(form.cleaned_data['category1'], allow_unicode=True)})
                post.categories.add(category1)

            if form.cleaned_data['category2'] != "":
                category2, created = Category.objects.get_or_create(
                    name=form.cleaned_data['category2'],
                    defaults={'slug': slugify(form.cleaned_data['category2'], allow_unicode=True)})
                post.categories.add(category2)

            post.save()

            return redirect(reverse('quotes-home'))
    else:
        form = PostForm()

    return render(request, 'quotes/post_form.html', {'form': form})


@login_required
def preview_post(request):
    if request.method == 'POST':
        quote = request.POST.get('quote')
        author = request.POST.get('author')
        category1 = request.POST.get('category1')
        category2 = request.POST.get('category2')
        background1 = request.POST.get('background1')
        background2 = request.POST.get('background2')

        if '\n' in quote:
            quote = quote.replace('\n', '<br>')

        data = {'quote': quote, 'author': author, 'category1': category1, 'category2': category2,
                'background1': background1, 'background2': background2}

        return render(request, 'quotes/post_preview.html', data)

    else:
        return HttpResponse('')


@login_required
def update_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            author, created = Author.objects.get_or_create(
                name=form.cleaned_data['author'],
                defaults={'slug': slugify(form.cleaned_data['author'], allow_unicode=True)})

            post.quote = form.cleaned_data['quote']
            post.author = author

            post.save()

            post.backgrounds.clear()

            background1, created = Background.objects.get_or_create(
                color=form.cleaned_data['background1'],
                defaults={'slug': slugify(form.cleaned_data['background1'], allow_unicode=True)})

            post.backgrounds.add(background1)

            background2, created = Background.objects.get_or_create(
                color=form.cleaned_data['background2'],
                defaults={'slug': slugify(form.cleaned_data['background2'], allow_unicode=True)})

            post.backgrounds.add(background2)

            post.categories.clear()

            if form.cleaned_data['category1'] != "":
                category1, created = Category.objects.get_or_create(
                    name=form.cleaned_data['category1'],
                    defaults={'slug': slugify(form.cleaned_data['category1'], allow_unicode=True)})
                post.categories.add(category1)

            if form.cleaned_data['category2'] != "":
                category2, created = Category.objects.get_or_create(
                    name=form.cleaned_data['category2'],
                    defaults={'slug': slugify(form.cleaned_data['category2'], allow_unicode=True)})
                post.categories.add(category2)

            post.save()

            return redirect(reverse('quotes-home'))
    else:
        categories = post.categories.all()
        backgrounds = post.backgrounds.all()

        if 2 == len(categories):
            category1 = categories[0].name
            category2 = categories[1].name
        elif len(categories) == 1:
            category1 = categories[0].name
            category2 = ""
        else:
            category1 = ""
            category2 = ""

        if len(backgrounds) == 2:
            background1 = backgrounds[0].color
            background2 = backgrounds[1].color
        elif len(categories) == 1:
            background1 = backgrounds[0].color
            background2 = ""
        else:
            background1 = ""
            background2 = ""

        form = PostForm(
            initial={'id': post.id, 'author': post.author.name, 'quote': post.quote, 'category1': category1,
                     'category2': category2,
                     'background1': background1, 'background2': background2})

    return render(request, 'quotes/post_form.html', {'form': form})


@login_required
def like_post(request, pk, like_val):
    if request.method == "POST":
        post = get_object_or_404(Post, id=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)

            if like.value != like_val:
                like.delete()

                new_like = Like()

                new_like.user = request.user
                new_like.post = post
                new_like.value = like_val

                if like_val == 1 and like.value != 1:
                    post.likes += 1
                elif like_val == 0 and like.value != 0:
                    post.likes -= 1
                    if post.likes <= 0:
                        post.likes = 0

                new_like.save()

                post.save()

                return redirect(reverse('quotes-home'))

        except Like.DoesNotExist:
            new_like = Like()

            new_like.user = request.user
            new_like.post = post
            new_like.value = like_val

            new_like.save()

            if like_val == 1:
                post.likes += 1
                post.save()

        return redirect(reverse('quotes-home'))


def about(request):
    return render(request, 'quotes/about.html')


def community(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'quotes/community.html', context)
