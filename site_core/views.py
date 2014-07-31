# -*- coding: utf-8 -*-
# Create your views here.

from models import Post, Category, Page, Parameter
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from default_site.settings import POST_PER_PAGE, DESCRIPTION, KEYWORDS, SITE_NAME


def get_child_pages(page_id):
    if Page.objects.filter(parent_page_id=page_id, published=True, in_menu=True).order_by('priority'):
        child_list = []
        child_dict = {}
        for child_page in Page.objects.filter(parent_page_id=page_id, published=True, in_menu=True).order_by('priority'):
            child_dict['name'] = child_page.title
            child_dict['slug'] = child_page.slug
            child_dict['child'] = get_child_pages(child_page.id)
            child_list.append(child_dict.copy())
        return child_list
    else:
        return None



def show_home(request, page=1):

    if page is not None:
        if int(page) == 0:
            page = 1

    posts_list = Post.objects.filter(published=True, attached=False).order_by('-post_date')
    paginator = Paginator(posts_list, POST_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    attached_posts = Post.objects.filter(attached=True, published=True).order_by('-post_date')
    meta = {'keywords': KEYWORDS,
            'description': DESCRIPTION,
            'sitename': SITE_NAME,
            'title': ''}

    return render_to_response('parts/home.html', {'posts': posts,
                                                  'attached_posts': attached_posts,
                                                  'meta': meta}, context_instance=RequestContext(request))


def show_post(request, req_slug):
    try:
        post = Post.objects.get(slug='/post/%s/' % req_slug, published=True)
    except ObjectDoesNotExist:
        raise Http404

    meta = {'keywords': post.keywords,
            'description': post.description,
            'sitename': '%s | %s' % (post.title, unicode(SITE_NAME, 'utf-8')),
            'title': ''}

    return render_to_response('parts/post.html', {'post': post,
                                                  'meta': meta}, context_instance=RequestContext(request))


def show_page(request, req_slug):
    try:
        page = Page.objects.get(slug='/page/%s/' % req_slug, published=True)
    except ObjectDoesNotExist:
        raise Http404

    meta = {'keywords': page.keywords,
            'description': page.description,
            'sitename': '%s | %s' % (page.title, unicode(SITE_NAME, 'utf-8')),
            'title': ''}

    return render_to_response('parts/page.html', {'page': page,
                                                  'meta': meta}, context_instance=RequestContext(request))


def show_tag_posts(request, tag_name, page=1):

    if page is not None:
        if int(page) == 0:
            page = 1

    posts_list = Post.objects.filter(tags__slug='/tag/%s/' % tag_name, published=True).order_by('-post_date')
    paginator = Paginator(posts_list, POST_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    meta = {'keywords': KEYWORDS,
            'description': DESCRIPTION,
            'sitename': SITE_NAME,
            'title': ''}

    return render_to_response('parts/tag_posts.html', {'posts': posts,
                                                       'tag': Post.tags.get(slug='/tag/%s/' % tag_name),
                                                       'meta': meta}, context_instance=RequestContext(request))


def show_category_posts(request, name, page=1):

    if page is not None:
        if int(page) == 0:
            page = 1

    posts_list = Category.objects.get(slug='/category/%s/' % name).post_set.filter(published=True).order_by('-post_date')
    paginator = Paginator(posts_list, POST_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    meta = {'keywords': KEYWORDS,
            'description': DESCRIPTION,
            'sitename': SITE_NAME,
            'title': ''}

    return render_to_response('parts/category_posts.html', {'posts': posts,
                                                            'category': Category.objects.get(slug='/category/%s/' % name),
                                                            'meta': meta}, context_instance=RequestContext(request))


def show_robots_file(request):
    try:
        parameter = Parameter.objects.get(name='robots.txt')
    except ObjectDoesNotExist:
        raise Http404
    if parameter.enable:
        return HttpResponse(parameter.value, content_type='text/plain')
    else:
        raise Http404


def search(request):
    if request.method == 'GET':
        if request.GET['search-text']:
            if request.GET.has_key('page'):
                page = request.GET['page']
            else:
                page = 1

            search_text = request.GET['search-text']
            posts_list = Post.objects.filter(Q(title__icontains=search_text) | Q(body__icontains=search_text) | Q(keywords__icontains=search_text) | Q(description__icontains=search_text)).order_by('-post_date')

            paginator = Paginator(posts_list, POST_PER_PAGE)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            meta = {'keywords': KEYWORDS,
                    'description': DESCRIPTION,
                    'sitename': SITE_NAME,
                    'title': ''}

            return render_to_response('parts/search.html', {'posts': posts,
                                                            'search_dict': {'text': search_text, 'slug': '/search/'},
                                                            'meta': meta}, context_instance=RequestContext(request))




def ajax_json(request):
    if request.GET.get('id') == 'tag':

        tag_list = []
        for tag in Post.tags.all():
            tag_list.append({'name': tag.name, 'slug': tag.slug, 'count': Post.objects.filter(tags__id=tag.id).count()})
        return HttpResponse(json.dumps(tag_list, ensure_ascii=False))

    elif request.GET.get('id') == 'category':

        category_list = []
        for category in Category.objects.all().order_by('priority'):
            category_list.append({'name': category.name, 'slug': category.slug})
        return HttpResponse(json.dumps(category_list, ensure_ascii=False))
    elif request.GET.get('id') == 'page_menu':
        full_list = []
        item_dict = {}
        for page_top in Page.objects.filter(parent_page_id=None, published=True, in_menu=True).order_by('priority'):
            item_dict['name'] = page_top.title
            item_dict['slug'] = page_top.slug
            item_dict['child'] = get_child_pages(page_top.id)
            full_list.append(item_dict.copy())
        return HttpResponse(json.dumps(full_list, ensure_ascii=False))

    else:
        raise Http404

