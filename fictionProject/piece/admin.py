from django.contrib import admin
from models import Piece, Character, Event#, Membership

class PieceAdmin(admin.ModelAdmin):
    pass

class CharacterAdmin(admin.ModelAdmin):
    pass
class EventAdmin(admin.ModelAdmin):
    pass
'''
class MembershipAdmin(admin.ModelAdmin):
    pass
'''

admin.site.register(Piece, PieceAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Event, EventAdmin)
# admin.site.register(Membership, MembershipAdmin)
