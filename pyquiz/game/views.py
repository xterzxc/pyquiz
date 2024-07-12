from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Player
import json

def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_name = data.get('name')
        host_name = data.get('host')

        if Room.objects.filter(name=room_name).exists():
            return JsonResponse({'error': 'Room already exists'}, status=400)

        room = Room(name=room_name, host=host_name, active=True)
        room.save()
        Player.objects.create(name=host_name, room=room)
        return JsonResponse({'success': 'Room created successfully'})

    return render(request, 'index.html')

def game(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
        players = Player.objects.filter(room=room)
    except Room.DoesNotExist:
        return HttpResponse('Room does not exist', status=404)
    
    
    return render(request, 'game.html', {
        'room_name': room_name,
        'players': players
    })
