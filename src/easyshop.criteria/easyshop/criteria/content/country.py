# zope imports
from zope.interface import implements
from zope.component import queryUtility

# Zope imports
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# Plone imports
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer.interfaces import IIDNormalizer

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import ICountryCriteria
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    LinesField(
        name='countries',
        multiValued=1,
        vocabulary="_getCountriesAsDL",
        widget=MultiSelectionWidget(
            label='Countries',
            label_msgid='schema_value_label',
            i18n_domain='EasyShop',
        ),
    ),

),
)

class CountryCriteria(BaseContent):
    """
    """
    implements(ICountryCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Country"

    def getValue(self):
        """
        """
        return ", ".join(self.getCountries())

    def _getCountriesAsDL(self):
        """
        """
        dl = DisplayList()
        for country in IShopManagement(self).getShop().getCountries():
            country = safe_unicode(country)
            term_value = queryUtility(IIDNormalizer).normalize(country)
            dl.add(term_value, country)

        return dl

registerType(CountryCriteria, PROJECTNAME)
