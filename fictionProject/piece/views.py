# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.forms.util import ErrorList

from forms import PieceForm, EventForm, CharacterForm
from models import *

def index(request):
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
    if request.method == 'GET' and not request.is_ajax():
        context['form'] = CharacterForm()
        character_name_list = []
        for character in Piece.objects.get(pk=pk).characters.all():
            full_name = character.__unicode__().replace('  ', ' ')
            character_name_list.append(character.id)
        eventForm = EventForm(aPiece)
        context['event_form'] = eventForm
    elif request.method == 'POST' and not request.is_ajax():
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
    elif request.is_ajax():
        context = {}
        if request.method == 'POST':
            if 'changePieceTitle' in request.POST:
                aPiece = Piece.objects.get(pk=pk)
                newTitle = request.POST['changePieceTitle']
                if newTitle and not aPiece.title == newTitle:
                    aPiece.title = newTitle
                    aPiece.save()
                context['changePieceTitle'] = aPiece.title
                data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')
    print('events: ',context['events'])
    return render(request, 'piece.html', context)

def event(request,p_pk,e_pk):
    context = {}
    context['p_pk'] = p_pk
    context['pieceTitle'] = Piece.objects.get(pk=p_pk).title
    context['path'] = request.get_full_path()
    if request.method == 'GET' and not request.is_ajax():
        anEvent = Event.objects.get(pk=e_pk)
        context['event'] = anEvent
        context['characters'] = anEvent.characters.all()
        context['form'] = EventForm(Piece.objects.get(pk=p_pk))
        context['allCharacters'] = Piece.objects.get(pk=p_pk).characters.all()
    elif request.method == 'POST' and not request.is_ajax():
        form = EventForm(request.POST)
        if form.is_valid():
            theEvent = Event.objects.get(pk=e_pk)
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            context['form'] = EventForm()
            if len(name):
                theEvent.name = name
            if len(description):
                theEvent.description = description
            if len(location):
                theEvent.location = location
            theEvent.save()
            context['event'] = theEvent
            context['characters'] = Character.objects.filter(events=e_pk)
        else:
            context['event'] = theEvent
            context['characters'] = Character.objects.filter(events=e_pk)
            context['form'] = EventForm(data=request.POST)
    elif request.is_ajax():
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            theEvent = Event.objects.get(pk=e_pk)
            changed = False
            if 'name' in request.POST:
                name = request.POST['name']
                if not name == theEvent.name and len(name):
                    theEvent.name = name
                    changed = True
                if changed:
                    theEvent.save()
                if name:
                    context['name'] = theEvent.name
            elif 'description' in request.POST:
                description = request.POST['description']
                if not description == theEvent.description and len(description):
                    theEvent.description = description
                    changed = True
                if changed:
                    theEvent.save()
                if description:
                    context['description'] = theEvent.description
            elif 'charName' in request.POST:
                name = request.POST['charName']
                character = Character.objects.get(name=name)
                if character in theEvent.characters.all():
                    theEvent.characters.remove(character)
                if character.name:
                    context['charName'] = None
            elif 'addCharacter' in request.POST:
                name = request.POST['addCharacter']
                character = Character.objects.get(name=name)
                if not character in theEvent.characters.all():
                    theEvent.characters.add(character)
                if character.name:
                    context['addCharacter'] = None
            elif 'e_order' in request.POST:
                e_order = request.POST['e_order']
                theEvent.order = e_order
                theEvent.save()
                context['e_order'] = theEvent.order
            data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')
    return render(request, 'event.html',context)

def eventTiming(request,pk):
    context = {}
    context['events'] = Piece.objects.get(pk=pk).events.all().order_by('order')
    context['pieceTitle'] = Piece.objects.get(pk=pk).title
    context['piecePK'] = pk
    return render(request,'eventTiming.html',context)
def characters(request,p_pk,ch_pk):
    context = {}
    context['character'] = Character.objects.get(pk=ch_pk)
    context['pieceTitle'] = Piece.objects.get(pk=p_pk).title
    context['piecePK'] = p_pk
    context['genderOptions'] = ['Male','Female']
    if request.is_ajax():
        if request.method == 'POST':
            context = {}
            if 'changeCName' in request.POST:
                c = Character.objects.get(pk=ch_pk)
                c_name = request.POST['changeCName']
                c.name = c_name
                c.save()
                context['c_name'] = c.name
            elif 'changeCAge' in request.POST:
                c = Character.objects.get(pk=ch_pk)
                c_age = request.POST['changeCAge']
                c.age = c_age
                c.save()
                context['changeCAge'] = c.age
            elif 'changeCGender' in request.POST:
                c = Character.objects.get(pk=ch_pk)
                c_gender = request.POST['changeCGender']
                c.gender = c_gender
                c.save()
                context['changeCGender'] = c.gender

            data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')
    return render(request, 'character.html', context)
