from django.contrib import admin
from models import Piece

class PieceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Piece, PieceAdmin)
