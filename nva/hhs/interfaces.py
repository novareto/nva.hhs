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


class IHazard(interface.Interface):

    id = schema.TextLine(
        title=u"ID",
        readonly=True
    )

    type = schema.Choice(
        title=u"Type of Hazard",
        source=sources('hazards'),
    )

    timespan = schema.Choice(
        title=u"Timespan",
        source=sources('timespans'),
    )


class IProduct(interface.Interface):

    id = schema.Int(
        title=u"ID",
        readonly=True
    )

    name = schema.TextLine(
        title=u"Name"
    )

    producer = schema.Choice(
        title=u"i",
        source=sources('producers'),
        required=False,
    )

    category = schema.Set(
        title=u"Category",
        value_type=schema.Choice(title=u"", source=sources('categories')),
    )

    hazards = schema.List(
        title=u"Hazards",
        value_type=schema.Object(title=u"", schema=IHazard),
    )


