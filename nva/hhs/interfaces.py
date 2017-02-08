# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from zope import interface, schema
from zope.component import getMultiAdapter
from zope.schema.interfaces import IContextSourceBinder
from collective.z3cform.datagridfield import IDataGridField
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import IDataConverter, IObjectFactory, NO_VALUE
from z3c.form.object import getIfName
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


class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

    
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
        source=sources('producers_query'),
        required=False,
    )

    categories = schema.Set(
        title=_(u"Category"),
        value_type=schema.Choice(title=_(u""), source=sources('categories')),
    )

    hazards = ListField(
        title=_(u"Hazards"),
        value_type=schema.Object(title=_(u""), schema=IHazard),
    )


class GridDataConverter(grok.MultiAdapter, BaseDataConverter):
    """Convert between the AddressList object and the widget. 
       If you are using objects, you must provide a custom converter
    """
    
    grok.adapts(ListField, IDataGridField)
    grok.implements(IDataConverter)

    def toWidgetValue(self, value):
        """Simply pass the data through with no change"""
        rv = list()
        for row in value:
            d = dict()
            for name, field in schema.getFieldsInOrder(
                    self.field.value_type.schema):
                d[name] = getattr(row, name)
            rv.append(d)
        return rv

    def toFieldValue(self, value):
        rv = list()
        
        for row in value:
            d = dict()

            name = getIfName(self.field.value_type.schema)
            factory = getMultiAdapter(
            (self.widget.context, self.widget.request,
             self.widget.form, self.widget), IObjectFactory,
                name=name).factory
            
            for name, field in schema.getFieldsInOrder(
                    self.field.value_type.schema):
                if row.get(name, NO_VALUE) != NO_VALUE:
                    d[name] = row.get(name)
            rv.append(factory(**d))
        return rv
