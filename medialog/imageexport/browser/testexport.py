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
        self.filename = "previewimages"
    
    def __call__(self,*args,**kwargs):
        '''Returns the file
        '''
        
        tmpfile = 'previewimages.tmp'
        filename = self.filename
        
        
        
        # Add header
        
        dataLen = len(tmpfile)
        setHeader = self.request.response.setHeader
        setHeader('Content-Length', dataLen)
        setHeader('Content-Type', 'text/csv')
        setHeader('Content-Disposition', 'attachment; filename=%s' % filename)
        
        return tmpfile
    
    
    
    
    
    

