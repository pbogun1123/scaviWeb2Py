# Scavi-Hunt Tables
# auth_user in db.py

db.define_table(
    'scavenger_hunt',
    Field('name', 'text', requires = IS_NOT_EMPTY()),
    Field('start_time', 'date', requires = IS_NOT_EMPTY()),
    Field('end_time', 'date', requires = IS_NOT_EMPTY()))

db.define_table(
    'clue',
    Field('hunt_id', 'reference scavenger_hunt'),
    Field('question', 'text', requires = IS_NOT_EMPTY()),
    Field('answer', 'text', requires = IS_NOT_EMPTY()),
    Field('points', 'integer', requires = IS_NOT_EMPTY(), default = 5),
    Field('latitude', 'double', requires = IS_NOT_EMPTY()),
    Field('longitude', 'double', requires = IS_NOT_EMPTY()),
    Field('clue_number', 'integer', requires = IS_NOT_EMPTY()))

db.clue.hunt_id.requires = IS_IN_DB(db, db.scavenger_hunt.id, '%(name)s')

db.define_table(
    'scavi_session',
    Field('user_id', 'reference auth_user', requires = IS_NOT_EMPTY()),
    Field('hunt_id', 'reference scavenger_hunt'),
    Field('next_clue_id', 'reference clue'),
    Field('current_clue_number', 'integer', default = 0),
    Field('points', 'integer', default = 0),
    Field('is_in_progress', 'boolean', default=True))

db.scavi_session.user_id.requires = IS_IN_DB(db, db.auth_user.id,
                                    '%(last_name)s, %(first_name)s')
db.scavi_session.hunt_id.requires = IS_IN_DB(db, db.scavenger_hunt.id, '%(name)s')
db.scavi_session.next_clue_id.requires = IS_IN_DB(db, db.clue.id, '%(question)s')

db.define_table(
    'guidePost',
    Field('postTitle', requires = IS_NOT_EMPTY(), label="Title"),
    Field('postContent', 'text', requires = IS_NOT_EMPTY(), label="Content"),
    Field('postAuthor', 'reference auth_user', label="Author"),
    Field('postDate', 'date', requires = IS_NOT_EMPTY(), label="Date"))

