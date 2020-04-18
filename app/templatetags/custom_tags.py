from django import template

register = template.Library()


@register.filter(name="class")
def add_css(field, classname):
    return field.as_widget(attrs={'class': classname})