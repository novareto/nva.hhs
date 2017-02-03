# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from zope import interface, schema
from zope.schema.interfaces import IContextSourceBinder
from collective.z3cform.datagridfield import DictRow
from . import VOCABULARIES
from . import MessageFactory as _


def sources(name):
    @grok.provider(IContextSourceBinder)
    def named_source(context):
        return VOCABULARIES[name](context)
    return named_source


class IProducer(interface.Interface):

    id = schema.Int(
        title=_(u"ID"),
        readonly=True
    )

    name = schema.TextLine(
        title=_(u"Name"),
    )

    street = schema.TextLine(
        title=_(u"Street"),
    )

    zip = schema.TextLine(
        title=_(u"ZIP"),
    )

    city = schema.TextLine(
        title=_(u"City"),
    )

    www = schema.TextLine(
        title=_(u"Hompage"),
    )

    email = schema.TextLine(
        title=_(u"E-Mail"),
    )

    products = schema.List(
        title=_(u"i"),
        value_type=schema.Choice(source=sources('products')),
        required=False,
    )


class IHazard(interface.Interface):

    id = schema.TextLine(
        title=_(u"ID"),
    )

    type = schema.Choice(
        title=_(u"Type of Hazard"),
        source=sources('hazards'),
    )

    timespan = schema.Choice(
        title=_(u"Timespan"),
        source=sources('timespans'),
    )


class ICategory(interface.Interface):

    id = schema.TextLine(
        title=_(u"ID"),
    )

    name = schema.TextLine(
        title=_(u"Name"),
    )


class IProduct(interface.Interface):

    id = schema.Int(
        title=_(u"ID"),
        readonly=True,
    )

    name = schema.TextLine(
        title=_(u"Name"),
    )

    product_id = schema.TextLine(
        title=_(u"ProductNumber")
    )

    producer = schema.Choice(
        title=_(u"Producer"),
        source=sources('producers'),
        required=False,
    )

    categories = schema.Set(
        title=_(u"Category"),
        value_type=schema.Choice(title=_(u""), source=sources('categories')),
    )

    hazards = schema.List(
        title=_(u"Hazards"),
        value_type=DictRow(title=_(u""), schema=IHazard),
    )


