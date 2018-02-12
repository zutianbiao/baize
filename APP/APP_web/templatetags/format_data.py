#!/usr/local/baize/env/bin/python
#  coding:utf-8

###################################################################################################
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@stringfilter
@register.filter(needs_autoescape=True)
def format_alarm_method(value, autoescape=True):
    list_alarm_method = [u'仅短信', u'仅邮件', u'短信与邮件']
    return list_alarm_method[value]


@stringfilter
@register.filter(needs_autoescape=True)
def format_alarm_switch(value, autoescape=True):
    if value:
        return 'checked'
    else:
        return ''

@stringfilter
@register.filter(needs_autoescape=True)
def format_alarm_switch_true_or_false(value, autoescape=True):
    if value:
        return 'true'
    else:
        return 'false'