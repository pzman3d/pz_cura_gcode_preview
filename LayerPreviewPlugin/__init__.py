from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("LayerPreviewPlugin")

from . import LayerPreviewPlugin

def getMetaData():
    return {}

def register(app):
    return {"extension": LayerPreviewPlugin.LayerPreviewPlugin()}
