import json

from django.shortcuts import render
from django.http import HttpResponse

from subject.models import Character
from piece.models import Piece
from models import Event

from piece.forms import EventForm

# Create your views here.
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