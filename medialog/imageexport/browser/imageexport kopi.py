# coding: utf-8

# Python imports
import os
import tempfile
import zipfile
import types

from zope import interface
from zope import component
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from tempfile import TemporaryFile
#from Products.CMFPlone.utils import getToolByName

class Exporter(BrowserView):
    
    def __init__(self, context, request):
        super(Exporter, self).__init__(context, request)
        self.filename = "previewimages"
    
    def __call__(self,*args,**kwargs):
        '''Returns the file (with the preview images
        '''
        #filename = self.filename
        
    
        # Write ZIP archive
        zip_filename = tempfile.mktemp()
        ZIP = zipfile.ZipFile(zip_filename, 'w')

        for obj in self.context.getFolderContents():
            obj = obj.getObject()

            if obj.portal_type == 'Image':
                # export only preview scale
                img = obj.Schema().getField('image').getScale(obj,scale='preview')
                ZIP.writestr('images/' + obj.getId() + ".jpg", str(img.data))
        
        ZIP.close()
        data = file(zip_filename).read()
        os.unlink(zip_filename) 
        R = self.request.RESPONSE
        R.setHeader('content-type', 'application/zip')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s.zip"' % self.context.getId())
        return R.write(data) 




    
    
    

