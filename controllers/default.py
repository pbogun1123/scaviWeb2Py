# -*- coding: utf-8 -*-

def index():
    """ Main Page """
    allGuides = db.guidePost
    guideRows = db(allGuides).select(orderby = db.guidePost.postDate)
    
    postQuery = db.guidePost.postTitle
    rows = db(postQuery).select(orderby = db.guidePost.postTitle)
    return dict(rows = rows, guideRows = guideRows)

def guidePost_CLICK():
    guide_id = request.args(0, cast=int)
    guide = db.guidePost(guide_id) or redirect (URL('index'))
    guideQuery = db(db.guidePost.id).select()
    return dict(guideQuery = guideQuery, guide = guide)

    
def user_admin():
    """ Administration page for editing users """
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

def user_CLICK():
    """ Auto generate page for each user in user search """
    user_id = request.args(0, cast=int)
    user = db.auth_user(user_id) or redirect (URL('index'))
    query = db(db.auth_user.id).select()
    return dict(query = query, user = user)

def hunt_admin():
    """ Administration page for editing scavenger hunts """
    scaviQuery = db.scavenger_hunt.name
    rows = db(scaviQuery).select(orderby=db.scavenger_hunt.name)
    return dict(rows = rows)

def hunt_admin_CLICK():
    """ Loads individual page for selected scavenger hunt """
    scavenger_id = request.args(0, cast=int)
    
    scavengerHunt = db.scavenger_hunt(scavenger_id) or redirect(URL('hunt_admin'))
    scavengerUsers = db.scavi_session(scavenger_id) or redirect(URL('hunt_admin'))

    # TODO: FIX REFERENCING IN FORMS!

    huntForm = SQLFORM(db.scavenger_hunt, scavengerHunt, deletable=True)
    huntUsersForm = SQLFORM(db.scavi_session, scavengerUsers, deletable=True)
    
    return dict(scavengerHunt = scavengerHunt, huntForm = huntForm, huntUsersForm = huntUsersForm)

########## API CALLS ##########


#TODO: Incorporate all API calls!


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


#@auth.requires_login() 
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
