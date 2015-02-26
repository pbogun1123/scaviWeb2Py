# -*- coding: utf-8 -*-

########## Main Pages ##########

def index():
    """ Main view of application """
    """ Contains group documentation and application guides """
    allGuides = db.guidePost
    guideRows = db(allGuides).select(orderby = db.guidePost.postDate)
    
    postQuery = db.guidePost.postTitle
    rows = db(postQuery).select(orderby = db.guidePost.postTitle)
    return dict(rows = rows, guideRows = guideRows)

#@auth.requires_login()
def hunt_admin():
    """ Administration page for viewing/editing scavenger hunts """
    scaviQuery = db.scavenger_hunt.name
    rows = db(scaviQuery).select(orderby=db.scavenger_hunt.name)
    return dict(rows = rows)

#@auth.requires_login()
def user_admin():
    """ Administration page for viewing/editing users """
    allUsers = db.auth_user
    userRows = db(allUsers).select(orderby = db.auth_user.last_name)
    
    form = SQLFORM.factory(Field('keyword', requires=IS_NOT_EMPTY())).process()
    if form.accepted:
        query = (((db.auth_user.first_name.contains(form.vars.keyword)) |
                (db.auth_user.last_name.contains(form.vars.keyword))))
        rows = db(query).select(orderby = db.auth_user.last_name)
    else:
        rows = ''
    return dict(form=form, rows=rows, userRows = userRows)

def googleMap():
    """ Uses google maps to get most accurate coordinates for scavenger sessions """
    """ This was moved to clue_EDIT as that is where the coordinates functionality """
    """ is needed most! If you want to re-use re-add to the menu in model/menu.py file """

    from gluon.tools import geocode
    latitude = longtitude = ''
    form=SQLFORM.factory(Field('search'), _class='form-search')
    form.custom.widget.search['_class'] = 'input-long search-query'
    form.custom.submit['_value'] = 'Search'
    form.custom.submit['_class'] = 'btn'
    if form.accepts(request):
        address=form.vars.search
        (latitude, longitude) = geocode(address)
    else:
        (latitude, longitude) = ('','')
    return dict(form=form, latitude=latitude, longitude=longitude)

########## _CLICK Pages ##########

#@auth.requires_login()
def guidePost_CLICK():
    """ Loads individual page for selected front page post """
    guide_id = request.args(0, cast=int)
    guide = db.guidePost(guide_id) or redirect (URL('index'))
    guideQuery = db(db.guidePost.id).select()
    return dict(guideQuery = guideQuery, guide = guide)

#@auth.requires_login()
def hunt_admin_CLICK():
    """ Loads individual page for selected scavenger hunt """
    scavenger_id = request.args(0, cast=int)
    scavengerHunt = db.scavenger_hunt(scavenger_id) or redirect(URL('hunt_admin'))
    
    clueQuery = db.clue.hunt_id==scavenger_id
    clueRows = db(clueQuery).select()
    
    sessionQuery = db.scavi_session.hunt_id==scavenger_id
    sessionRows = db(sessionQuery).select()

    return dict(scavengerHunt = scavengerHunt, clueRows = clueRows,
                sessionRows = sessionRows)

#@auth.requires_login()
def user_CLICK():
    """ Loads individual page for selected user """
    user_id = request.args(0, cast=int)
    user = db.auth_user(user_id) or redirect (URL('index'))
    query = db(db.auth_user.id).select()
    return dict(query = query, user = user)

########## _EDIT Pages ##########

def guidePost_EDIT():
    """ Edit page for selected guide post """
    selectedPost = db.guidePost(request.args(0))
    postForm = SQLFORM(db.guidePost, selectedPost, deletable=True)
    if postForm.process().accepted:
        response.flash = 'Edit Sucessful'
    elif postForm.errors:
        response.flash = 'Edit Failure'
    return dict(postForm = postForm)

def hunt_admin_EDIT():
    """ Edit page for selected scavenger hunt """
    selectedHunt = db.scavenger_hunt(request.args(0))
    huntForm = SQLFORM(db.scavenger_hunt, selectedHunt, deletable=True)
    if huntForm.process().accepted:
        response.flash = 'Edit Sucessful'
    elif huntForm.errors:
        response.flash = 'Edit Failure'
    return dict(huntForm = huntForm)

def clue_EDIT():
    """ Edit page for selected clue """
    from gluon.tools import geocode

    selectedClue = db.clue(request.args(0))
    clueForm = SQLFORM(db.clue, selectedClue, deletable=True)
    if clueForm.process().accepted:
        response.flash = 'Edit Sucessful'
    elif clueForm.errors:
        response.flash = 'Edit Failure'
    
    latitude = longtitude = ''
    form=SQLFORM.factory(Field('search'), _class='form-search')
    form.custom.widget.search['_class'] = 'input-long search-query'
    form.custom.submit['_value'] = 'Search'
    form.custom.submit['_class'] = 'btn'
    if form.accepts(request):
        address=form.vars.search
        (latitude, longitude) = geocode(address)
    else:
        (latitude, longitude) = ('','')

    return dict(form=form, latitude=latitude, longitude=longitude,
                clueForm = clueForm)

def session_EDIT():
    """ Edit page for selected session """
    selectedSession = db.scavi_session(request.args(0))
    sessionForm = SQLFORM(db.scavi_session, selectedSession, deletable=True)
    if sessionForm.process().accepted:
        response.flash = 'Edit Sucessful'
    elif sessionForm.errors:
        response.flash = 'Edit Failure'
    return dict(sessionForm = sessionForm)

########## _CREATE Pages ##########

def clue_CREATE():
    from gluon.tools import geocode

    clueCreate = SQLFORM(db.clue)
    if clueCreate.process().accepted:
        response.flash = 'form accepted'
    elif clueCreate.errors:
        response.flash = 'form has errors'

    latitude = longtitude = ''
    form=SQLFORM.factory(Field('search'), _class='form-search')
    form.custom.widget.search['_class'] = 'input-long search-query'
    form.custom.submit['_value'] = 'Search'
    form.custom.submit['_class'] = 'btn'
    if form.accepts(request):
        address=form.vars.search
        (latitude, longitude) = geocode(address)
    else:
        (latitude, longitude) = ('','')
    return dict(form=form, latitude=latitude, longitude=longitude,
                clueCreate = clueCreate)

def hunt_admin_CREATE():
    scavengerCreate = SQLFORM(db.scavenger_hunt)
    if scavengerCreate.process().accepted:
        response.flash = 'form accepted'
    elif scavengerCreate.errors:
        response.flash = 'form has errors'
    return dict(scavengerCreate = scavengerCreate)

def session_CREATE():
    scavSessionCreate = SQLFORM(db.scavi_session)
    if scavSessionCreate.process().accepted:
        response.flash = 'form accepted'
    elif scavSessionCreate.errors:
        response.flash = 'form has errors'
    return dict(scavSessionCreate = scavSessionCreate)

def guidePost_CREATE():
    documentCreate = SQLFORM(db.guidePost)
    if documentCreate.process().accepted:
        response.flash = 'form accepted'
    elif documentCreate.errors:
        response.flash = 'form has errors'
    return dict(documentCreate = documentCreate)
    

########## REST CALLS ##########

def userREST():
    """ Use to get .json format for specified user """
    """ http://127.0.0.1:8000/ScaviHunt/default/userREST/154 """
    """ http://127.0.0.1:8000/ScaviHunt/default/userREST.json/154 """
    user_id = request.args(0, cast=int)
    user = db.auth_user(user_id)
    return dict (user = user)

def scavengerHuntREST():
    """ Use to get .json format for specified scavenger hunt """
    scavenger_id = request.args(0, cast=int)
    scavengerHunt = db.scavenger_hunt(scavenger_id)
    return dict (scavengerHunt = scavengerHunt)

def clueREST():
    """ Use to get .json format for specified clue """
    clue_id = request.args(0, cast=int)
    clue = db.clue(clue_id)
    return dict(clue = clue)

def scaviSessionREST():
    """ Use to get .json format for specified scavenger session """
    session_id = request.args(0, cast=int)
    scavengerSession = db.scavi_session(session_id)
    return dict (scavengerSession = scavengerSession)

########## Extras ##########

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
