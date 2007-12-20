# Zope imports
from zope.interface import implements

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IInformationContainer

class InformationContainer(OrderedBaseFolder, ATCTMixin):
    """A simple container to hold information like terms and conditions.
    """
    implements(IInformationContainer)

registerType(InformationContainer, PROJECTNAME)