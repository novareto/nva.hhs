# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


from uvc.api import api
from zope import interface
from nva.hhs.content import container, models


api.templatedir('templates')


class LandingPage(api.Page):
    api.context(interface.Interface)


class ProducersOverview(api.Page):
    api.context(container.Producers)
    api.name('index')


class ProductsOverview(api.Page):
    api.context(container.Products)
    api.name('index')


class ProducerDisplay(api.Page):
    api.context(models.Producer)
    api.name('index')


class ProductDisplay(api.Page):
    api.context(models.Product)
    api.name('index')
