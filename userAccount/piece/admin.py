from django.contrib import admin
from piece.models import Piece

class PieceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Piece, PieceAdmin)
