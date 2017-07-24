# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):
	posts = Post.published.all()
	ctx = {
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