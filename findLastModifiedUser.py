from AccessControl.SecurityManagement import newSecurityManager
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest
from zope.app.component.hooks import setSite

app = makerequest(app)

app._p_jar.sync()

site=app['Plone']

setSite(site)

admin = app.acl_users.getUserById('admin')
admin = admin.__of__(app.acl_users)
newSecurityManager(None, admin) 

portal_catalog = getToolByName(site, "portal_catalog")
pr = getToolByName(site, "portal_repository")

now = DateTime()

results = portal_catalog.searchResults({'modified' : {'query' : now - 1, 'range' : 'min'}})

for r in results:
    o = r.getObject()
    history = pr.getHistoryMetadata(o)
    if history:
        revisions = history.getLength(countPurged=False)
        vdatafull = history.retrieve(revisions-1, countPurged=False)
        vdata = vdatafull['metadata']
        modifier = vdata['sys_metadata']['principal']
        print o.absolute_url()
        print modifier
        print "\n"
