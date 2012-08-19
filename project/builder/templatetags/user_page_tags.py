# Import Django
from django import template

# Import models
from ..models import *

register = template.Library()

@register.simple_tag
def get_element(user_page, identifier):
	element = user_page.get_element(identifier)
	return element if element else ''
	
@register.simple_tag
def get_setting(user_page, identifier):
	setting = user_page.get_setting(identifier)
	return setting if setting else ''

@register.simple_tag
def get_template_data(user_page, identifier):
	template_data = user_page.get_template_data(identifier)
	return template_data if template_data else ''