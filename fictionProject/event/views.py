import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import UpdateView


from subject.models import Character
from piece.models import Piece
from models import Event

from piece.forms import EventForm

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': form.instance.pk,
            }
            return self.render_to_json_response(data)
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)

class EventDetailView(AjaxableResponseMixin, UpdateView):
    model = Event
    context_object_name='event'
    template_name = 'event.html'
    def get_context_data(self, **kwargs):
        e_pk = self.kwargs['e_pk']
        p_pk = self.kwargs['p_pk']

        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['p_pk'] = p_pk
        context['pieceTitle'] = Piece.objects.get(pk=p_pk).title
        #context['path'] = request.get_full_path()

        #context['Name'] = get_object_or_404(Event,id=self.kwargs['e_pk']).name
        context['eventPK'] = get_object_or_404(Event,id=self.kwargs['e_pk']).id
        context['event'] = get_object_or_404(Event,id=self.kwargs['e_pk'])
        context['characters'] = context['event'].characters.all()
        context['form'] = EventForm(Piece.objects.get(pk=p_pk))
        context['allCharacters'] = Piece.objects.get(pk=p_pk).characters.all()
        context['piece'] = get_object_or_404(Piece, id=p_pk)
        return context
        
    def get_object(self):
        event = get_object_or_404(Event, id=self.kwargs['e_pk'])
        return event
    '''    
    def get(self,request,*args,**kwargs):
        context = self.get_context_data()
        character = self.get_object()
        return self.render_to_response(context)
    '''
        
    def post(self,request,*args,**kwargs):
        #context = super(CharacterDetailView,self).get_context_data(**kwargs)
        context = {}
        if 'e_name' in request.POST:
            new_name = request.POST['e_name']
            event = self.get_object()
            if event in Event.objects.all():
                if not new_name == event.name and len(new_name):
                    event.name = new_name
                    event.save()
                    context['e_name'] = event.name
        elif 'description' in request.POST:
            new_description = request.POST['description']
            event = self.get_object()
            if event in Event.objects.all():
                if not new_description == event.description and len(new_description):
                    event.description = new_description
                    event.save()
                    context['description'] = event.description
        elif 'charName' in request.POST:
            name = request.POST['charName']
            character = Character.objects.get(name=name)
            event = self.get_object()
            if event in Event.objects.all():
                if character in event.characters.all():
                    event.characters.remove(character)
                if character.name:
                    context['charName'] = None


        elif 'addCharacter' in request.POST:
            name = request.POST['addCharacter']
            event = self.get_object()
            if event in Event.objects.all():
                character = Character.objects.get(name=name)
                if not character in event.characters.all():
                    event.characters.add(character)
                if character.name:
                    context['addCharacter'] = None

        elif 'e_order' in request.POST:
            e_order = request.POST['e_order']
            event = self.get_object()
            if event in Event.objects.all():
                event.order = e_order
                event.save()
                context['e_order'] = event.order

        if context:
            return self.render_to_json_response(context)




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
