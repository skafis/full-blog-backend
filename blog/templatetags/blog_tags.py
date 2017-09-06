import markdown
from django import template 
from django.db.models import Count
from django.utils.safestring import mark_safe

register = template.Library()
from ..models import Post

@register.simple_tag
def total_posts():
	return Post.published.count()

@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	print (latest_posts)
	ctx={
	'latest_posts': latest_posts
	}
	return ctx

@register.assignment_tag
def get_most_commented_posts(count=5):
	return Post.published.annotate(
				total_comments=Count('comments')
				).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_formart(text):
	return mark_safe(markdown.markdown(text))