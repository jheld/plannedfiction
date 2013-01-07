import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import UpdateView

from models import Character
from event.models import Event
from piece.models import Piece

from piece.forms import CharacterForm

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


class CharacterDetailView(AjaxableResponseMixin, UpdateView):
    model = Character
    context_object_name='character'
    template_name = 'character.html'
    def get_context_data(self, **kwargs):
        context = super(CharacterDetailView, self).get_context_data(**kwargs)
        context['pieceTitle'] = get_object_or_404(Piece,id=self.kwargs['p_pk']).title
        context['piecePK'] = get_object_or_404(Piece,id=self.kwargs['p_pk']).id
        return context
        
    def get_object(self):
        character = get_object_or_404(Character, id=self.kwargs['ch_pk'])
        return character
    '''    
    def get(self,request,*args,**kwargs):
        context = self.get_context_data()
        character = self.get_object()
        return self.render_to_response(context)
    '''
        
    def post(self,request,*args,**kwargs):
        #context = super(CharacterDetailView,self).get_context_data(**kwargs)
        context = {}
        new_name = request.POST['changeCName']
        print(new_name)
        character = self.get_object()
        if character in Character.objects.all():
            character.name = new_name
            character.save()
            context['c_name'] = character.name
        return self.render_to_json_response(context)
    

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
