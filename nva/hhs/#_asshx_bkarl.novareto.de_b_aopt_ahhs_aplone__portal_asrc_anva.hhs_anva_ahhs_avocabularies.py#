# -*- coding: utf-8 -*-

import grokcore.component as grok
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from z3c.saconfig import named_scoped_session
from .content.models import Product, Producer
from . import VOCABULARIES


@grok.provider(IContextSourceBinder)
def products(context):
    items = []
    session = named_scoped_session('sqlsession')
    for product in session.query(Product).all():
        items.append(SimpleTerm(
            product, token=product.id, title=product.name))
    return SimpleVocabulary(items)


@grok.provider(IContextSourceBinder)
def producers(context):
    items = []
    session = named_scoped_session('sqlsession')
    for producer in session.query(Producer).all():
        items.append(SimpleTerm(
            producer, token=producer.id, title=producer.name))
    return SimpleVocabulary(items)


VOCABULARIES['products'] = products
VOCABULARIES['producers'] = producers
