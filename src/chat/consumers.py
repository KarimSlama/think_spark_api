import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from register.models import Profile
from core.notifications import send_notification

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.room_group_name = 'chat_global'

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
            conversation_id = data.get('conversation_id')
            user_id = data.get('user_id')
            recipient_id = data.get('recipient_id')
            
            if not message or not user_id:
                return await self.send_error("Message and user_id are required")

            user = await self.get_user_with_profile(user_id)
            if not user:
                return await self.send_error("User not found")

            if not conversation_id:
                if not recipient_id:
                    return await self.send_error("recipient_id is required for new conversations")
                
                conversation = await self.create_conversation(user_id, recipient_id)
                if not conversation:
                    return await self.send_error("Failed to create conversation")
            else:
                conversation = await self.get_conversation(conversation_id)
                if not conversation:
                    if recipient_id:
                        conversation = await self.create_conversation(user_id, recipient_id)
                        if not conversation:
                            return await self.send_error("Failed to create conversation")
                    else:
                        return await self.send_error("Conversation not found and no recipient_id provided")

            message_obj = await self.save_message(conversation, user, message)

            profile_image = None
            try:
                if user.profile.image:
                    profile_image = user.profile.image.url
            except Profile.DoesNotExist:
                pass

            response = {
                "success": True,
                "message": "Message sent successfully",
                "conversation_id": conversation.id,
                "data": {
                    "id": message_obj.id,
                    "text": message_obj.text,
                    "timestamp": message_obj.timestamp.isoformat(),
                    "sender": {
                        "id": user.id,
                        "username": user.username,
                        "image": profile_image,
                        "bio": user.profile.bio if hasattr(user, 'profile') else None
                    }
                }
            }

            await self.send_notifications_to_recipients(
                conversation=conversation,
                sender=user,
                message_text=message,
                sender_image=profile_image
            )

            await self.send(json.dumps(response))

        except Exception as e:
            await self.send_error(f"Server error: {str(e)}")

    @database_sync_to_async
    def create_conversation(self, user1_id, user2_id):
        try:
            user1 = User.objects.get(id=user1_id)
            user2 = User.objects.get(id=user2_id)
            
            existing_conv = Conversation.objects.filter(
                participants=user1
            ).filter(
                participants=user2
            ).distinct().first()
            
            if existing_conv:
                return existing_conv
                
            conversation = Conversation.objects.create()
            conversation.participants.add(user1, user2)
            
            welcome_message = Message.objects.create(
                conversation=conversation,
                sender=user1,
                text="New Conversation started"
            )
            
            return conversation
        
        except User.DoesNotExist:
            print(f"One of the users not found: {user1_id} or {user2_id}")
            return None
        except Exception as e:
            print(f"Error creating conversation: {str(e)}")
            return None

    async def send_error(self, error_message):
        await self.send(json.dumps({
            "success": False,
            "message": error_message
        }))


    @database_sync_to_async
    def send_notifications_to_recipients(self, conversation, sender, message_text, sender_image=None):
        recipients = conversation.participants.exclude(id=sender.id)

        profile = Profile.objects.first()
        if profile and profile.device_token:
            send_notification(
                token=profile.device_token,
                title="Test from Django Shell",
                body="This is a test notification"
            )
        
        for recipient in recipients:
            try:
                if hasattr(recipient, 'profile') and recipient.profile.device_token:
                    token = recipient.profile.device_token.strip()
                    print(f"Attempting to send to token: {token}")
                    
                    title = f"New Message from {sender.username}"
                    body = message_text
                    
                    data = {
                        'conversation_id': str(conversation.id),
                        'sender_id': str(sender.id),
                        'type': 'chat_message'
                    }
                    
                    success = send_notification(token, title, body, data)
                    if success:
                        print(f"Notification sent to {recipient.username}")
                    else:
                        print(f"Failed to send to {recipient.username}")
            except Exception as e:
                print(f"Error sending to {recipient.username}: {str(e)}")

    @database_sync_to_async
    def get_user_with_profile(self, user_id):
        try:
            return User.objects.select_related('profile').get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, conversation, user, text):
        return Message.objects.create(
            conversation=conversation,
            sender=user,
            text=text
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))