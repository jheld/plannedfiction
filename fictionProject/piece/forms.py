from django import forms
from models import Piece


class PieceForm(forms.Form):
    title = forms.CharField(max_length=100)

class EventForm(forms.Form):
    name = forms.CharField(max_length=250, required=True)
    description = forms.CharField(max_length=250,widget=forms.widgets.Textarea(),required=False)
    dateTime = forms.DateTimeField(required=False)
    location = forms.CharField(max_length=250,required=False)
    characters = forms.MultipleChoiceField(choices=[],required=False)
    def __init__(self, p,*args, **kwargs):
        super(EventForm,self).__init__(*args,**kwargs)
        self.fields['characters'] = forms.MultipleChoiceField(choices=[(c.id, str(c)) for c in p.characters.all()] )

class CharacterForm(forms.Form):
    first_name = forms.CharField(max_length=20,required=False)
    middle_name = forms.CharField(max_length=20,required=False)
    last_name = forms.CharField(max_length=30,required=False)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=30)
    
