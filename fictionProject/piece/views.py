# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.forms.util import ErrorList

from forms import PieceForm, EventForm, CharacterForm
from models import *

def index(request):
    context = {}
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
    context['events'] = aPiece.events.all()
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
            new_fName = form.cleaned_data['first_name']
            new_mName = form.cleaned_data['middle_name']
            new_lName = form.cleaned_data['last_name']
            new_age = form.cleaned_data['age']
            new_gender = form.cleaned_data['gender']
            newCharacter = Character.objects.create(first_name=new_fName,middle_name=new_mName,last_name=new_lName,age=new_age,gender=new_gender)
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
                if Event.objects.all():
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
            print('got here!')
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
                mName = ''
                if len(name.split(' ')) == 3:
                    mName = name.split(' ')[1]
                character = Character.objects.get(first_name=name.split(' ')[0],middle_name=mName,last_name=name.split(' ')[-1])
                if character in theEvent.characters.all():
                    theEvent.characters.remove(character)
                '''
                for c in theEvent.characters.all():
                    if c.pk == character.pk:
                        theEvent.characters.remove(c)
                        break
                '''
                if name:
                    context['charName'] = None
            elif 'addCharacter' in request.POST:
                name = request.POST['addCharacter']
                mName = ''
                if len(name.split(' ')) == 3:
                    mName = name.split(' ')[1]
                character = Character.objects.get(first_name=name.split(' ')[0],middle_name=mName,last_name=name.split(' ')[-1])
                if not character in theEvent.characters.all():
                    theEvent.characters.add(character)
                if name:
                    context['addCharacter'] = None

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
    if request.is_ajax():
        if request.method == 'POST':
            context = {}
            if 'changeCName' in request.POST:
                c = Character.objects.get(pk=ch_pk)
                c_name_piece = request.POST['changeCName']
                name_type = request.POST['name_type']
                if name_type == 'c_fName':
                    c.first_name = c_name_piece
                    c.save()
                    context['c_name_piece'] = c.first_name

                elif name_type == 'c_mName':
                    c.middle_name = c_name_piece
                    c.save()
                    context['c_name_piece'] = c.middle_name
                elif name_type == 'c_lName':
                    c.last_name = c_name_piece
                    c.save()
                    context['c_name_piece'] = c.last_name
            data = json.dumps(context)
            return HttpResponse(data,mimetype='application/json')
    return render(request, 'character.html', context)
