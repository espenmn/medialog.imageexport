from Products.PythonScripts.standard import html_quote
request = container.REQUEST
resp = request.RESPONSE

vocab = context.listMetaDataFields(False)
fields = context.getCustomViewFields()

counter = 0
print '|'.join([vocab.getValue(field, field) for field in fields])

for brain in context.queryCatalog():
  results = []
  for field in fields:
    val = getattr(brain, field, '')
    try:
      results.append(val.pCommonZ())
    except:
      if hasattr(val, 'append'):
        results.append(', '.join(val))
      elif val is None:
        results.append('')
      else:
        results.append(str(val))

#  print results
  print '|'.join(results)

resp.setHeader("Content-type","application/vnd.ms-excel")
resp.setHeader("Content-disposition","attachment;filename=" + context.getId() + ".csv")

return printed