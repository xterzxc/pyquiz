import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Player
from asgiref.sync import sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"room_{self.room_name}"
        self.player_name = None

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if self.player_name:
            room = await sync_to_async(Room.objects.get)(name=self.room_name)
            await sync_to_async(Player.objects.filter(name=self.player_name, room=room).delete)()

            players = await sync_to_async(list)(Player.objects.filter(room=room).values_list('name', flat=True))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_players',
                    'players': players
                }
            )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'join_room':
            await self.handle_join_room(data)

    async def handle_join_room(self, data):
        self.player_name = data['player_name']
        room = await sync_to_async(Room.objects.get)(name=self.room_name)
        player, created = await sync_to_async(Player.objects.get_or_create)(name=self.player_name, room=room)

        players = await sync_to_async(list)(Player.objects.filter(room=room).values_list('name', flat=True))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_players',
                'players': players
            }
        )

    async def update_players(self, event):
        players = event['players']
        await self.send(text_data=json.dumps({
            'type': 'update_players',
            'players': players
        }))
