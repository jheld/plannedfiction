# Create your views here.
import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.generic import ListView, FormView
from django.views.generic.edit import FormMixin,ProcessFormView

from piece.forms import PieceForm, EventForm, CharacterForm
from piece.models import Piece
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
            return HttpResponse(data,content_type='application/json')

    return render(request,'index.html',context)


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



class PiecesListView(AjaxableResponseMixin,FormMixin,ListView):
    queryset = Piece.objects.all()
    context_object_name = 'pieces'
    template_name = 'pieces.html'
    model = Piece
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = PieceForm
        self.form = self.get_form(form_class)
        
        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)
        
    def post(self, request, *args, **kwargs):
        
        form_class = PieceForm
        self.form = self.get_form(form_class)
        new_title = self.form.data['newTitle']
        context = {}
        if not len(Piece.objects.filter(title=new_title)):
            newPiece = Piece.objects.create(title=new_title)
            newPiece.save()
            context['pieceTitle'] = newPiece.title
            context['piecePK'] = newPiece.pk
        #return self.get(request, *args, **kwargs)
        return self.render_to_json_response(context)

    
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
                full_name = str(character).replace('  ', ' ')
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
            return HttpResponse(data,content_type='application/json')
    return render(request, 'piece.html', context)




    
