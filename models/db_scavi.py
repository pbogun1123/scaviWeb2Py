
# Finalize and finish tables
# Fix references

db.define_table(
    'scavi_session',
    Field('user_id', 'reference auth_user'),
    Field('hunt_id', 'reference scavenger_hunt'),
    Field('next_clue_id', 'reference clue'),
    Field('points', 'integer'),
    Field('is_in_progress', 'boolean', default=False))

db.define_table(
    'scavenger_hunt',
    Field('name', 'text', requires = IS_NOT_EMPTY()),
    Field('start_time', 'date', requires = IS_NOT_EMPTY()),
    Field('end_time', 'date', requires = IS_NOT_EMPTY()),
    )

db.define_table(
    'clue',
    )
