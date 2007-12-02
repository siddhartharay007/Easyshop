# Zope imports
from zope.interface import implements
from zope.component import adapts

# AdvancedQuery
from Products.AdvancedQuery import Eq
 
# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShop

class CategoryCategoryManagement:
    """Adapter which provides ICategoryManagement for category content 
    objects.
    """
    implements(ICategoryManagement)
    adapts(ICategory)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """
        query = Eq("portal_type", "Category") & \
                Eq("path", "/".join(self.context.getPhysicalPath())) & \
                ~ Eq("id", self.context.getId())
        
        
        catalog = getToolByName(self.context, "portal_catalog")
        
        brains = catalog.evalAdvancedQuery(
                        query, ("getObjPositionInParent", ))

        return brains
                                  
    def getTopLevelCategories(self):
        """Returns brains
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Category",
            path = {"query"       : "/".join(self.context.getPhysicalPath()),
                    "depth"       : 1},
        )

        return brains
        
class ProductCategoryManagement:
    """Adapter which provides ICategoryManagement for product content objects.
    """
    implements(ICategoryManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """    
        raise Exception
        
    def getTopLevelCategories(self):
        """Returns objects.
        """
        # Need the try/except here, because the of the temporary created
        # shipping product, which has no context and hence no access to 
        # tools and catalogs (and it doesn't need it, but I have to catch 
        # the error.)
        try:
            mtool = getToolByName(self.context, "portal_membership")            
            categories = self.context.getBRefs("category_products")
        except AttributeError:
            return []

        result = []
        for category in categories:
            if mtool.checkPermission("View", category):
                result.append(category)
            
        return result
        
class ShopCategoryManagement:
    """An adapter which provides ICategoryManagement for shop content objects.
    """
    implements(ICategoryManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.categories = context.categories

    def getCategories(self):
        """Returns brains
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.categories.getPhysicalPath()),
            portal_type="Category",
            sort_on = "getObjPositionInParent")

        return brains
    
    def getTopLevelCategories(self):
        """Return brains.
        """ 
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(portal_type="Category",
                         path = {"query" : "/".join(self.categories.getPhysicalPath()),
                                 "depth" : 1},
                         sort_on = "getObjPositionInParent")

        return brains