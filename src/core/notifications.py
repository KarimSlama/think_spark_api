import firebase_admin
from firebase_admin import credentials, messaging
import os
from pathlib import Path

# Try to initialize Firebase only if credentials file exists
if not firebase_admin._apps:
    # Try multiple possible paths for Firebase credentials
    possible_paths = [
        os.path.join('E:/Django Projects/think-spark-1c5d6-firebase-adminsdk-fbsvc-976e200044.json'),
        os.path.join(Path(__file__).resolve().parent.parent.parent, 'think-spark-1c5d6-firebase-adminsdk-fbsvc-976e200044.json'),
        os.environ.get('FIREBASE_CREDENTIALS_PATH'),
    ]
    
    cred_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            cred_path = path
            break
    
    if cred_path:
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Warning: Failed to initialize Firebase Admin: {e}")
    else:
        print("Warning: Firebase credentials file not found. Notifications will not work.")

def send_notification(token, title, body, data=None):
    # Check if Firebase is initialized
    if not firebase_admin._apps:
        print("Warning: Firebase Admin not initialized. Cannot send notification.")
        return False
    
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