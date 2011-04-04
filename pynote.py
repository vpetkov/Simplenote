#!/usr/bin/env python
#-*- coding UTF-8 -*-

import simplenote

user = simplenote.User('mail@example.com', '')

index = simplenote.Index(user)

note = simplenote.Note(user)
note.key = 'agtzaW1wbGUtbm90ZXINCxIETm90ZRic6'
note.update()
print unicode(note)
