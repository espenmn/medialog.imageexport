from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.imageexport')

def format_size(size):
    return "".join(size).split(' ')[0]


def ImageSizeVocabulary(context):
    sizes = []
    terms = []
        
    try:
        #Plone 5
        sizes = api.portal.get_registry_record('plone.allowed_sizes')
    except: 
        #Plone 4
        portal_properties = api.portal.get_tool(name='portal_properties')
        if 'imaging_properties' in portal_properties.objectIds():
            sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')

    if sizes:
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
        

    return SimpleVocabulary(terms)
    
directlyProvides(LeadImageSizeVocabulary, IVocabularyFactory)