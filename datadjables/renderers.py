from django.template import Template


def simple(colname):
    return Template(u'{{{{ obj.{f} }}}}'.format(f=colname))
