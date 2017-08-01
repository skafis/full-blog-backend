# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.
def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3) 
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page not an integer show first page
		posts = paginator.page(1)
	except EmptyPage:
		# f page is out of range show last page of results
		posts = paginator.page(paginator.num_pages)
	ctx = {
	'page':page,
	'posts':posts,
	}
	return render(request,
				'blog/post/list.html',
				ctx
				)

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
									status='published',
									publish__year = year,
									publish__month=month,
									publish__day=day)
	ctx ={
		'post':post,
		}
	return render(request,
					'blog/post/detail.html',
					ctx)