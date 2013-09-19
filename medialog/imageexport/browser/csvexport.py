# coding: utf-8

from zope import interface
from zope import component
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.utils import getToolByName


from tempfile import TemporaryFile



class Exporter(BrowserView):
    
    def __init__(self, context, request):
        super(Exporter, self).__init__(context, request)
        
    def __call__(self, REQUEST):
        '''Returns the csv file, 
        '''
        thefields = self.request.get('fields', 'title')  #Using only titleif none is defined
        request = self.request
        context = self.context
        
        # get the data
        L = thefields.split(', ')
        CSV = []
        
        for obj in self.context.getFolderContents():
            obj = obj.getObject()
            
            for field in L:     
                #import p db; p db.set_trace() #use dir(thisfield)
                #field_id = thisfield.__name__
                #field_value = thisfield.getAccessor(obj)()
                
                thisfield = obj.getField(field)
                field_value = thisfield.getRaw(obj)

                CSV.append(field_value)
        
        
        # Add header
        
        dataLen = len(CSV)
        R = self.request.RESPONSE
        R.setHeader('Content-Length', dataLen)
        R.setHeader('Content-Type', 'text/csv')
        R.setHeader('Content-Disposition', 'attachment; filename=%s.csv' % self.context.getId())
        
        #return thefields
        return CSV
    
    
    
