# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


from five import grok
from zope.interface import implementer, Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError
from zope.traversing.namespace import SimpleHandler
from nva.hhs.content import container


@implementer(IBrowserView)
class ProducerTraverser(SimpleHandler, grok.MultiAdapter):
    """ PRODUCER"""
    grok.name('producers')
    grok.adapts(Interface, Interface)
    grok.provides(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        objs = container.Producers(self.context, '++producers++', 'sqlsession')
        objs.__of__(self.context)
        if not name:
            return objs
        else:
            try:
                return objs[name]
            except KeyError:
                raise TraversalError(self.context, name)


@implementer(IBrowserView)
class ProductTraverser(SimpleHandler, grok.MultiAdapter):
    """ PRODUCT"""
    grok.name('products')
    grok.adapts(Interface, Interface)
    grok.provides(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        objs = container.Products(self.context, '++products++', 'sqlsession')
        objs.__of__(self.context)
        if not name:
            return objs
        else:
            try:
                return objs[name]
            except KeyError:
                raise TraversalError(self.context, name)
