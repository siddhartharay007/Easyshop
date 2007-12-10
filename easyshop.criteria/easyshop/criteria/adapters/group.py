# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IGroupCriteria
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class GroupCriteriaValidity:
    """Adapter which provides IValidity for group criteria content
    objects.
    """    
    implements(IValidity)
    adapts(IGroupCriteria)

    def __init__(self, context):
        """
        """        
        self.context = context
        
    def isValid(self, product=None):
        """Returns True, if given product is at least in one of the selected
           groups
        """
        product_groups = IGroupManagement(product).getGroups()
        criteria_groups = self.context.getGroups()

        for criteria_group in criteria_groups:
            if criteria_group in product_groups:
                return True
        return False
