from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# ---------------------------------------------------


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

    def update_rating(self, prat, crat):
        post_rat = self.post_set.aggregate(postrating=Sum('rating'))
        prat += post_rat.get('postrating')
        comment_rat = self.author_user.comment_set.aggregate(
            commentrating=Sum('rating'))
        crat += comment_rat.get('commentrating')
        self.rating_author = prat * 3 + crat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True, )
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=54)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:125] + '...'

    def __str__(self):
        return f'{self.pk} : {self.title} : {self.text} : {self.date_creation}'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
