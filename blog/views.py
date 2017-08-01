# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm, CommentForm

# Create your views here.
def post_list(request, tag_slug=None):
	object_list = Post.published.all()

	# tags 
	tag=None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])


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
	'tag':tag,
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
	#list all active comments of this post
	comments = post.comments.filter(active=True)

	if request.method == 'POST':
    #a comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
            #create comment
			new_comment = comment_form.save(commit=False)
			#assign current comment to post
			new_comment.post = post
			new_comment.save()
	else:
		comment_form  = CommentForm()


	# list of simillar posts
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids)\
								.exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
								.order_by('-same_tags','-publish')[:4]

	ctx ={
		'post':post,
		'comments':comments,
		'comment_form':comment_form,
		'similar_posts':similar_posts,
		}
	return render(request,
					'blog/post/detail.html',
					ctx)