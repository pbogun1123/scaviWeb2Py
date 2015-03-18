# -*- coding: utf-8 -*-

#################### Main Pages ####################

def index():
    """ Main view of application """
    """ Contains group documentation and application guides """
    allGuides = db.guidePost
    guideRows = db(allGuides).select(orderby = ~db.guidePost.postDate)
    postQuery = db.guidePost.postTitle
    rows = db(postQuery).select(orderby = db.guidePost.postTitle)
    return dict(rows = rows, guideRows = guideRows)

def hunt_admin():
    """ Administration page for viewing/editing scavenger hunts """
    scaviQuery = db.scavenger_hunt.name
    rows = db(scaviQuery).select(orderby=db.scavenger_hunt.name)
    return dict(rows = rows)

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
    """ is needed most. If you want to re-use, re-add to the menu in model/menu.py file """
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

#################### _CLICK Pages ####################

def guidePost_CLICK():
    """ Loads individual page for selected front page post """
    guide_id = request.args(0, cast=int)
    guide = db.guidePost(guide_id) or redirect (URL('index'))
    guideQuery = db(db.guidePost.id).select()
    return dict(guideQuery = guideQuery, guide = guide)

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

def user_CLICK():
    """ Loads individual page for selected user """
    user_id = request.args(0, cast=int)
    user = db.auth_user(user_id) or redirect (URL('index'))
    userSession = db.scavi_session.user_id == user_id
    userHunts = db(userSession).select()
    
    return dict(user = user, userHunts = userHunts)

#################### _EDIT Pages ####################

def guidePost_EDIT():
    """ Edit page for selected guide post """
    selectedPost = db.guidePost(request.args(0))
    postForm = SQLFORM(db.guidePost, selectedPost, deletable=True, showid=False)
    if postForm.process().accepted:
        redirect(URL(r=request, f='index'))
    elif postForm.errors:
        response.flash = 'Edit Failure'
    return dict(postForm = postForm)

def hunt_admin_EDIT():
    """ Edit page for selected scavenger hunt """
    selectedHunt = db.scavenger_hunt(request.args(0))
    huntForm = SQLFORM(db.scavenger_hunt, selectedHunt, deletable=True,
                       showid=False)
    if huntForm.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
    elif huntForm.errors:
        response.flash = 'Edit Failure'
    return dict(huntForm = huntForm)

def clue_EDIT():
    """ Edit page for selected clue """
    from gluon.tools import geocode
    selectedClue = db.clue(request.args(0))
    clueForm = SQLFORM(db.clue, selectedClue, deletable=True, showid=False)
    if clueForm.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
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
    sessionForm = SQLFORM(db.scavi_session, selectedSession, deletable=True,
                          showid=False)
    if sessionForm.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
    elif sessionForm.errors:
        response.flash = 'Edit Failure'
    return dict(sessionForm = sessionForm)

def user_EDIT():
    """ Edit page for selected user """
    db.auth_user.password.writable = False
    selectedUser = db.auth_user(request.args(0))
    userForm = SQLFORM(db.auth_user, selectedUser, deletable=True,
                       showid=False)
    if userForm.process().accepted:
        redirect(URL(r=request, f='user_admin'))
    elif userForm.errors:
        response.flash = 'Edit Failure'
    return dict(userForm = userForm)

#################### _CREATE Pages ####################

def clue_CREATE():
    """ Clue creation """
    from gluon.tools import geocode

    clueCreate = SQLFORM(db.clue)
    if clueCreate.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
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
    """ Scavenger hunt creation """
    scavengerCreate = SQLFORM(db.scavenger_hunt)
    if scavengerCreate.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
    elif scavengerCreate.errors:
        response.flash = 'form has errors'
    return dict(scavengerCreate = scavengerCreate)

def session_CREATE():
    """ Session creation for a scavenger hunt """
    scavSessionCreate = SQLFORM(db.scavi_session)
    if scavSessionCreate.process().accepted:
        redirect(URL(r=request, f='hunt_admin'))
    elif scavSessionCreate.errors:
        response.flash = 'form has errors'
    return dict(scavSessionCreate = scavSessionCreate)

def guidePost_CREATE():
    """ Creation of a guide post for index view """
    documentCreate = SQLFORM(db.guidePost)
    if documentCreate.process().accepted:
        redirect(URL(r=request, f='index'))
    elif documentCreate.errors:
        response.flash = 'form has errors'
    return dict(documentCreate = documentCreate)

#################### REST CALLS ####################

def applogin():
    """ REST call for user login, currently only login with a user's email """
    email = request.vars['email']
    
    logged_user = db((db.auth_user.email == email)).select()
    return dict(logged_user = logged_user)

def huntsession():
    """ REST call for retrieving each user's hunt sessions """
    user_id = request.vars['user_id']
    hunt_id = request.vars['hunt_id']
    query = ((db.scavi_session.hunt_id == hunt_id) & (db.scavi_session.user_id == user_id))
    usersession = db(query).select()
    clueQuery = db.clue.hunt_id==hunt_id
    clueRows = db(clueQuery).select()
    
    if len(usersession) < 1:
        id = db.scavi_session.insert(user_id=user_id, hunt_id=hunt_id)
        usersession = db((db.scavi_session.id == id)).select()
    
    return dict(session = usersession, rows=clueRows)

def updatesession():
    """ REST call for updating and storing each user's hunt sessions """
    user_id = request.vars['user_id']
    hunt_id = request.vars['hunt_id']
    current_clue_number = request.vars['current_clue_number']
    points = request.vars['points']
    
    query = ((db.scavi_session.hunt_id == hunt_id) & (db.scavi_session.user_id == user_id))
    usersession = db(query).update(current_clue_number=current_clue_number)
    
    return dict(status='success')

#################### Extras ####################

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
