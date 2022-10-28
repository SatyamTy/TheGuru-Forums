from distutils.text_file import TextFile
from email.policy import default
from tabnanny import verbose
from django.db.models.deletion import CASCADE
from unicodedata import category
from django.db import models
from django.forms import CharField
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse

User = get_user_model()

class Author(models.Model):
    title = models.CharField(max_length=50)
    title= "test"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=400, unique=False, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, blank=True)

    def __str__(self) -> str:
        return self.fullname

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Author, self).save()

class id_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField( max_length=50)
    Class = models.IntegerField(max_length=2)
    section =models.CharField( max_length=1)
    father_name=models.CharField( max_length=50)
    mother_name=models.CharField( max_length=50)
    mobile=models.IntegerField( max_length=10)
    Adress = HTMLField()
    pic = ResizedImageField(size=[100 , 160], quality=100, upload_to="id-pics", default=None, blank=True)    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    # class Meta:
    #     verbose_name_plural = "ids"

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")

    class Meta:
        verbose_name_plural = "categories"
    def __str__(self) -> str:
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save()

    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })

    @property
    def num_post(self):
        return Post.objects.filter(category=self).count()

    @property
    def last_post(self):
        return Post.objects.filter(category=self).latest("date")

class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[: 100]  

    class Meta:
        verbose_name_plural = "replies"

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[: 100]   

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    category = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=40, default="zero")

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save()

    def __str__(self) -> str:
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })

    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")

    @property
    def get_(self):
        return self.comments.latest("date")
