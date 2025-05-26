import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Route, WeatherImpact, TrafficImpact

class RouteUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_name = f"user_{self.user.id}_updates"
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'request_update':
            await self.send_route_updates()

    async def route_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_route_updates(self):
        return Route.objects.filter(user=self.user).order_by('-created_at')[:5]

    async def send_route_updates(self):
        routes = await self.get_route_updates()
        await self.send(text_data=json.dumps({
            'type': 'route_updates',
            'routes': [self.format_route(route) for route in routes]
        }))

    def format_route(self, route):
        return {
            'id': route.id,
            'source': route.source,
            'destination': route.destination,
            'distance': route.distance,
            'fuel_consumption': route.fuel_consumption,
            'carbon_emissions': route.carbon_emissions,
            'created_at': route.created_at.isoformat()
        }