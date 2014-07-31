# -*- coding: utf-8 -*-
from django.db import models

from pytils.translit import slugify as translate_slug

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, Tag
# Create your models here.


class PostTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        slug = '/tag/%s/' % translate_slug(unicode(tag))
        if i is not None:
            slug += '-%d' % i
        return slug


class PostTaggedItem(TaggedItemBase):
    content_object = models.ForeignKey('Post')

    @classmethod
    def tag_model(self):
        return PostTag


class Post(models.Model):

    author = models.CharField('Автор', blank=True, max_length=512)
    post_date = models.DateTimeField('Время создания')
    title = models.CharField('Заголовок', max_length=512)
    body = RichTextField(config_name='awesome_ckeditor', verbose_name='Текст' )
    body_split = models.TextField(blank=True, default='')
    read_more = models.BooleanField(default=False)
    tags = TaggableManager(verbose_name='Теги', through=PostTaggedItem)
    categories = models.ForeignKey('Category', verbose_name='Категория')
    slug = models.CharField('Slug', blank=True, null=True, max_length=512, default=None)
    description = models.CharField('Описание', max_length=512, blank=True, default=None)
    keywords = models.CharField('Ключевые слова', max_length=512, blank=True, default=None)
    published = models.BooleanField('Опубликовано?', default=True)
    attached = models.BooleanField('Прикрепить на главную?', default=False)

    def __unicode__(self):
        return self.title


    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        Post.objects.filter(id=self.id).update(slug='/post/%s/' % translate_slug(unicode(self.title)))

        Post.objects.filter(id=self.id).update(body_split=self.body.split('<!--more-->')[0])
        if Post.objects.get(id=self.id).body != Post.objects.get(id=self.id).body_split:
            Post.objects.filter(id=self.id).update(read_more=True)
        else:
            Post.objects.filter(id=self.id).update(read_more=False)


class Page(models.Model):

    author = models.CharField('Автор', blank=True, max_length=512)
    post_date = models.DateTimeField('Время создания')
    title = models.CharField('Заголовок', max_length=512)
    body = RichTextField(config_name='awesome_ckeditor', verbose_name='Текст')
    parent_page = models.ForeignKey('self', verbose_name='Родительская страница',  blank=True, null=True)
    slug = models.CharField('Slug', blank=True, null=True, max_length=512, default=None)
    description = models.CharField('Описание', max_length=512, blank=True, default=None)
    keywords = models.CharField('Ключевые слова', max_length=512, blank=True, default=None)
    published = models.BooleanField('Опубликовано?', default=True)
    priority = models.IntegerField('Приоритет', help_text='1 левее - 10 правее', blank=True, default=1)
    in_menu = models.BooleanField('Отображать в меню?', default=False)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        Page.objects.filter(id=self.id).update(slug='/page/%s/' % translate_slug(unicode(self.title)))


class Category(models.Model):
    name = models.CharField('Имя', max_length=512, default=None)
    slug = models.CharField('Slug', blank=True, null=True, max_length=512, default=None)
    priority = models.IntegerField('Приоритет', help_text='1 левее - 10 правее', blank=True, default=1)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.filter(id=self.id).update(slug='/category/%s/' % translate_slug(unicode(self.name)))


class Parameter(models.Model):
    enable = models.BooleanField("Enable", default=False)
    name = models.CharField('Name of parameter', max_length=512)
    value = models.TextField('Value of parameter', blank=True, default='')

    def __unicode__(self):
        return self.name