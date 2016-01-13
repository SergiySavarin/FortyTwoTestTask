from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def edit_link(obj):
    """Usage: {% edit_link object %}"""
    object_c = ContentType.objects.get_for_model(obj)
    try:
        url = reverse(
            'admin:%s_%s_change' % (object_c.app_label, object_c.model),
            args=(obj.id,)
        )
    except:
        return 'Error: object not registered in admin models'
    return url
