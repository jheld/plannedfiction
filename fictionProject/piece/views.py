# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from forms import PieceForm, EventForm, CharacterForm
from models import Piece
from event.models import Event
from subject.models import Character

def index(request):
    '''
    The homepage for the site. Includes a character search field for authenticated/logged in users.
    '''
    context = {}
    if request.is_ajax():
        if request.method == 'GET':
            if 'character_search_input' in request.GET:
                character_search = request.GET['character_search_input']
                characters_results = Character.objects.filter(name__contains=character_search)
                if characters_results:
                    formatted_results = []
                    for character_result in characters_results:
                        full_name = character_result.__unicode__().replace('  ', ' ')
                        for piece in Piece.objects.all():
                            if character_result in piece.characters.all():
                                formatted_results.append([full_name,piece.id,character_result.id,piece.title])
                    context['characters_results'] = formatted_results
                else:
                    context['characters_results'] = ['No results.']
            data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')

    return render(request,'index.html',context)
#@login_required
def pieces(request):
    context = {}
    context['pieces'] = Piece.objects.all()    
    if request.method == 'GET':
        context['form'] = PieceForm()
    elif request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            try:
                new_title = form.cleaned_data['title']
                newPiece = Piece.objects.create(title=new_title)
                newPiece.save()
                form = PieceForm()
            except:
                form._errors['title'] = ErrorList([u'Title must be unique!'])
            context['form'] = form

    return render(request,'pieces.html',context)
    
def piece(request,pk):
    context = {}
    aPiece = Piece.objects.get(pk=pk)
    context['events'] = aPiece.events.all().order_by('order')
    context['characters'] = aPiece.characters.all()
    context['piece'] = aPiece
    context['path'] = request.get_full_path()
    if not request.is_ajax():
        if request.method == 'GET':
            context['form'] = CharacterForm()
            character_name_list = []
            for character in Piece.objects.get(pk=pk).characters.all():
                full_name = character.__unicode__().replace('  ', ' ')
                character_name_list.append(character.id)
            eventForm = EventForm(aPiece)
            context['event_form'] = eventForm
        elif request.method == 'POST':
            form = CharacterForm(request.POST)
            if form.is_valid() and 'age' in request.POST:
                new_name = form.cleaned_data['name']
                new_age = form.cleaned_data['age']
                new_gender = form.cleaned_data['gender']
                newCharacter = Character.objects.create(name=new_name,age=new_age,gender=new_gender)
                newCharacter.save()
                aPiece = Piece.objects.get(pk=pk)
                aPiece.characters.add(newCharacter)
                context['form'] = CharacterForm()
                context['event_form'] = EventForm(aPiece)
            else:
                aPiece = Piece.objects.get(pk=pk)
                form = EventForm(aPiece,request.POST)
                if form.is_valid() and not 'age' in request.POST:
                    e_name = form.cleaned_data['name']
                    e_description = form.cleaned_data['description']
                    e_datetime = form.cleaned_data['dateTime']
                    e_location = form.cleaned_data['location']
                    if len(Event.objects.all()):
                        new_order = Event.objects.all().order_by('-order')[0].order+1
                    else:
                        new_order = 1
                    newEvent = Event.objects.create(name=e_name,description=e_description,time=e_datetime,location=e_location, order=new_order)
                    newEvent.save()
                    aPiece = Piece.objects.get(pk=pk)
                    aPiece.events.add(newEvent)
                    characters = form.cleaned_data['characters']
                    for char in characters:
                        newEvent.characters.add(Character.objects.get(pk=char))
                    context['event_form'] = EventForm(aPiece)
                    context['form'] = CharacterForm()
    else:
        context = {}
        if request.method == 'POST':
            if 'changePieceTitle' in request.POST:
                aPiece = Piece.objects.get(pk=pk)
                newTitle = request.POST['changePieceTitle']
                title_error = ''
                if Piece.objects.filter(title=newTitle):
                    title_error = '"{title}" Is taken! Not changing the title.'.format(title=newTitle)
                if not aPiece.title == newTitle and not title_error:
                    aPiece.title = newTitle
                    aPiece.save()
                context['changePieceTitle'] = aPiece.title
                context['title_error'] = title_error
                data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')
    return render(request, 'piece.html', context)




    
