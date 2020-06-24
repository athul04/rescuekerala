from django import template

register = template.Library()

# @register.simple_tag
# def get_list(hashtags):
#     return hashtags.split(',')


@register.filter(name="get_list")
def get_list(hashtags):
    if hashtags == "":
        return []

    return [i.strip() for i in hashtags.split(",")]
