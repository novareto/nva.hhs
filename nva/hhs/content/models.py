# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from bgetem.sqlcontainer.models import PloneModel
from bgetem.sqlcontainer.dexterity import ContentFTI, AddForm
from five import grok
from nva.hhs import interfaces
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from zope.interface import implementer
from .. import Base


@implementer(interfaces.IProducer)
class Producer(PloneModel, Base):
    grok.title("Producer")

    portal_type = "producer"
    __tablename__ = 'producers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    street = Column('street', String(50))
    zip = Column('zip', String(50))
    www = Column('hompage', String(50))
    email = Column('email', String(50))
    products = relation("Product", backref="producer")

    def getId(self):
        return self.name


class ProducerFTI(ContentFTI):
    grok.name('producer')
    __model__ = Producer
    schema = interfaces.IProducer
    klass = "nva.hhs.content.Producer"


class ProducerAddForm(AddForm):
    grok.name('producer')


@implementer(interfaces.IProduct)
class Product(PloneModel, Base):
    grok.title("Product")

    portal_type = "product"
    __tablename__ = 'products'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    category = Column('category', String(50))
    producer_id = Column('producer_id', Integer, ForeignKey('producers.id'))
    hazards = relation("Hazard", backref="product")
    
    def getId(self):
        return self.email


class ProductFTI(ContentFTI):
    grok.name('product')
    __model__ = Product
    schema = interfaces.IProduct
    klass = "nva.hhs.content.Product"


class ProductAddForm(AddForm):
    grok.name('product')


@implementer(interfaces.IHazard)
class Hazard(PloneModel, Base):
    grok.title("Hazard")

    portal_type = "hazard"
    __tablename__ = 'hazards'

    id = Column('id', Integer, primary_key=True)
    type = Column('name', String(50))
    timespan = Column('category', String(50))
    product_id = Column('product_id', Integer, ForeignKey('products.id'))

    def reindexObject(self, *args, **kwargs):
        pass

from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(interfaces.IHazard, Hazard)


class HazardFTI(ContentFTI):
    grok.name('hazard')
    __model__ = Hazard
    schema = interfaces.IHazard
    klass = "nva.hhs.content.Hazard"


class HazardAddForm(AddForm):
    grok.name('hazard')
