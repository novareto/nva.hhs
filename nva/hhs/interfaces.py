# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from zope import interface, schema
from zope.schema.interfaces import IContextSourceBinder
from . import VOCABULARIES


def sources(name):
    @grok.provider(IContextSourceBinder)
    def named_source(context):
        return VOCABULARIES[name](context)
    return named_source


class IProducer(interface.Interface):

    id = schema.Int(
        title=u"ID",
        readonly=True
    )

    name = schema.TextLine(
        title=u"Name"
    )

    street = schema.TextLine(
        title=u"Street"
    )

    zip = schema.TextLine(
        title=u"ZIP"
    )

    www = schema.TextLine(
        title=u"Hompage"
    )

    email = schema.TextLine(
        title=u"E-Mail"
    )

    products = schema.List(
        title=u"i",
        value_type=schema.Choice(source=sources('products')),
        required=False,
    )


class IProduct(interface.Interface):

    id = schema.Int(
        title=u"ID",
        readonly=True
    )

    name = schema.TextLine(
        title=u"Name"
    )

    category = schema.TextLine(
        title=u"Category"
    )

    producer = schema.Choice(
        title=u"i",
        source=sources('producers'),
        required=False,
    )
