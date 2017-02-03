# -*- coding: utf-8 -*-

import logging
from five import grok
from z3c.saconfig.interfaces import IEngineCreatedEvent
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from zope.interface import implementer
from z3c.saconfig import named_scoped_session
from zope.i18nmessageid import MessageFactory

MessageFactory = MessageFactory('nva.hhs')


Base = declarative_base()


logger = logging.getLogger('uvcsite.nva.hhs')


def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)


@grok.subscribe(IEngineCreatedEvent)
def create_engine_created(event):
    Base.metadata.create_all(event.engine)


VOCABULARIES = {}
