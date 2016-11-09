from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

from django.utils.text import slugify
# Create your models here.

def upload_location(obj, filename):
    return "{0}/{1}".format(obj.slug, filename)

class Post(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # used by python 2
    def __unicode__(self):
        return self.title

    # used in python 3
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-id', '-timestamp', '-updated']

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    query_set = Post.objects.filter(slug=slug).order_by('-id')
    if query_set.exists():
        new_slug = "{0}-{1}".format(slug, query_set.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reciever, sender=Post)