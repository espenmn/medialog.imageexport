# coding: utf-8

# Python imports
import os
import tempfile
import zipfile
 
from Products.Five import BrowserView
from tempfile import TemporaryFile
from plone.dexterity.utils import iterSchemata, resolveDottedName
from zope.schema import getFields
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import IImageScaleTraversable, INamedImageField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

class Exporter(BrowserView):
    
    index = ViewPageTemplateFile("imageexport.pt")
    
    
    def render(self):
        return self.index()

    def __init__(self, context, request):
        super(Exporter, self).__init__(context, request)
    
    def __call__(self,REQUEST):
        imagesize = self.request.get('imagesize')
        if 'imagesize' in self.request:
            self.export_images(imagesize.split()[0])
            return self.request.response.redirect(self.context.absolute_url())
        return self.index()

    def imagesizes(context):
        site = getSite()
    
        portal_properties = getToolByName(site, 'portal_properties', None)
        if 'imaging_properties' in portal_properties.objectIds():
            sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')
            return sizes
        else:
            return ['preview']


    def export_images(self, imagesize):
        '''Returns the file (with the preview images
        '''
        # Write ZIP archive
        zip_filename = tempfile.mktemp()
        ZIP = zipfile.ZipFile(zip_filename, 'w')
        
        #hack for new collection
        try:
        	all_folder_contents = self.context.results(batch=False)
        except AttributeError:
        	#for folder and old collection
        	all_folder_contents = self.context.getFolderContents()
        			
        for obj in all_folder_contents:
            obj = obj.getObject()
            try:
                #this is for archetype
                #imageformat is image/jpg so we are skipping the first part
                #this leaves us with png / jpg / gif or something else.
                imageformat = obj.getContentType()
                imageformat = imageformat.split("/")
                image_suffix = imageformat[1]
                #hack for news item image
                if image_suffix == 'html':
                    image_suffix = 'jpg'
                if image_suffix == 'jpeg':
                    image_suffix = 'jpg'

                full_image_name = obj.getId() + '.' + image_suffix

                img = obj.Schema().getField('image').getScale(obj,scale=imagesize)
                ZIP.writestr(self.context.getId() + '/' + full_image_name, str(img.data))
            except:
                #this is for dexterity blob fields
                if IDexterityContent.providedBy(obj):
                    for schemata in iterSchemata(obj):
                        for name, field in getFields(schemata).items():
                            #checking for image field
                            if INamedImageField.providedBy(field):
                                #copied this line from somewhere
                                field_value = field.get(field.interface(obj))
                                if field_value is not None:
                                    #field_value is not correct, this gets the image, not the scale
                                    ZIP.writestr(self.context.getId() + '/' + str((field_value.filename).encode("utf8")), str(field_value.data))
            finally:
                pass
        
        ZIP.close()
        data = file(zip_filename).read()
        os.unlink(zip_filename) 
        R = self.request.RESPONSE
        R.setHeader('content-type', 'application/zip')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s.zip"' % self.context.getId())
        return R.write(data)

        #return REQUEST.RESPONSE.redirect(context.absolute_url())






    
    
    

