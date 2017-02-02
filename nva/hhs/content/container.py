# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from bgetem.sqlcontainer.container import SQLContainer
from nva.hhs.content import models


class Producers(SQLContainer):
    model = models.Producer
    title = "Producers"
    
    def key_converter(self, id):
        return int(id)

    def allowedContentTypes(self):
        return [models.ProducerFTI]


class Products(SQLContainer):
    model = models.Product
    title = "Product"

    def key_converter(self, id):
        return int(id)

    def allowedContentTypes(self):
        return [models.ProductFTI]
