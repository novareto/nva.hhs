# -*- coding: utf-8 -*-

import grokcore.component as grok
import transaction

from sqlalchemy.exc import IntegrityError
from z3c.formwidget.query.interfaces import IQuerySource
from z3c.saconfig import named_scoped_session
from zope.processlifetime import IDatabaseOpenedWithRoot
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implementer

from . import VOCABULARIES
from .content.models import Product, Producer, Category


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


@implementer(IQuerySource)
class ProducersQuery(object):
    
    def __init__(self, context):
        self.vocabulary = producers(context)

    def __contains__(self, item):
        return self.vocabulary.__contains__(item)

    def __iter__(self):
        return iter(self.vocabulary)

    def getTerm(self, *args, **kwargs):
        return self.vocabulary.getTerm(*args, **kwargs)

    def getTermByToken(self, *args, **kwargs):
        return self.vocabulary.getTermByToken(*args, **kwargs)

    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.value.name.lower()]


@grok.provider(IContextSourceBinder)
def query_producers(context):
    return ProducersQuery(context)


@grok.provider(IContextSourceBinder)
def categories(context):
    items = []
    session = named_scoped_session('sqlsession')
    for cat in session.query(Category).all():
        items.append(SimpleTerm(
            cat, token=cat.id, title=cat.name))
    return SimpleVocabulary(items)


@grok.provider(IContextSourceBinder)
def hazards(context):
    items = []
    for hazard in [u'acid', 'heat', 'radioativ', 'bio']:
        items.append(SimpleTerm(
            hazard, token=hazard, title=hazard))
    return SimpleVocabulary(items)


@grok.provider(IContextSourceBinder)
def timespans(context):
    items = []
    for timespan in [u'0-1 Hours', '1-2 Hours', '3-4 Hours', '5-6 Hours']:
        items.append(SimpleTerm(
            timespan, token=timespan, title=timespan))
    return SimpleVocabulary(items)


VOCABULARIES['products'] = products
VOCABULARIES['producers'] = producers
VOCABULARIES['categories'] = categories 
VOCABULARIES['hazards'] = hazards 
VOCABULARIES['timespans'] = timespans
VOCABULARIES['producers_query'] = query_producers


CATEGORIES = [
    (u'mechanisch', u'Mechanisch'),
    (u'biologisch', u'Biologisch'),
    (u'chemisch', u'Chemisch'),
    (u'thermisch', u'Thermisch'),
    (u'strahlen', u'Strahlen'),
]

@grok.subscribe(IDatabaseOpenedWithRoot)
def create_sql_content(event):
    try:
        print "Injecting SQL content"
        with transaction.manager:
            session = named_scoped_session('sqlsession')
            for id, name in CATEGORIES:
                cat = Category(id=id, name=name)
                session.add(cat)
    except IntegrityError:
        # data already exists, skipping.
        print "SQL content was already created"
