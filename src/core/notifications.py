import firebase_admin
from firebase_admin import credentials, messaging
import os

if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(
        'E:/Django Projects/think-spark-1c5d6-firebase-adminsdk-fbsvc-976e200044.json'))
    firebase_admin.initialize_app(cred)

def send_notification(token, title, body, data=None):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {},
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default',
                        badge=1,
                        mutable_content=True,
                        category='NEW_MESSAGE_CATEGORY'
                    )
                )
            ),
        )
        
        response = messaging.send(message)
        print(f"Notification sent successfully. Message ID: {response}")
        return True
    except Exception as e:
        print(f"Failed to send notification. Error: {str(e)}")
        return False