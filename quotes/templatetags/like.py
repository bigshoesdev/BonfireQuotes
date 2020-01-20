from django import template

from quotes.models import Like

register = template.Library()


@register.simple_tag(takes_context=True)
def get_like(context, post):
    try:
        request = context['request']
        post = Like.objects.get(post=post, user=request.user)
        return post
    except Exception as e:
        return None

