import simplenote

user = simplenote.User('mail@vpetkov.com', 'pass')
note = simplenote.Note(user)

note.content = 'test note'
note.create()
note.content += '(to be deleted)\nsome more text added'
print note
note.merge()
note.delete()
note.restore()

