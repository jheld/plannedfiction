import json

from django.shortcuts import render
from django.http import HttpResponse
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from models import Character
from event.models import Event
from piece.models import Piece

from piece.forms import CharacterForm



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
