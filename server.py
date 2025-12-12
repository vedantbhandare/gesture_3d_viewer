import asyncio
import cv2
import mediapipe as mp
import math
import json
from aiohttp import web

# --- Global set of connected clients ---
connected_websockets = set()

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils # Helper to draw the skeleton
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# --- 1. WebSocket Handler ---
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("Client connected")
    connected_websockets.add(ws)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
    finally:
        connected_websockets.remove(ws)
        print('Client disconnected')
    
    return ws

# --- 2. Camera & Gesture Logic Loop ---
async def capture_and_process(app):
    cap = cv2.VideoCapture(0) 
    
    print("Starting Camera Loop... Check your taskbar for the popup window.")
    
    try:
        while True:
            # Yield control to allow web requests to process
            await asyncio.sleep(0.01)
            
            # NOTE: We removed the check "if not connected_websockets"
            # so the camera window stays open even if no browser is connected.

            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip image for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            data = {"gesture": "None", "zoom": 1.0, "rx": 0.0, "ry": 0.0}

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                # --- DRAW THE SKELETON ---
                # This draws the red lines/dots onto the 'frame' window
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                # --- LOGIC: Rotation (Index Finger Tip) ---
                index_tip = hand_landmarks.landmark[8]
                rx = (index_tip.y - 0.5) * 4 
                ry = (index_tip.x - 0.5) * 4
                
                # --- LOGIC: Zoom (Pinch) ---
                thumb_tip = hand_landmarks.landmark[4]
                dist = math.sqrt(
                    (thumb_tip.x - index_tip.x)**2 + 
                    (thumb_tip.y - index_tip.y)**2
                )
                zoom_factor = 1.0 + (dist * 2) 

                data = {
                    "gesture": "Tracking",
                    "zoom": round(zoom_factor, 2),
                    "rx": round(rx, 3),
                    "ry": round(ry, 3)
                }
                
                # Add Debug Text to the Video Feed
                cv2.putText(frame, f"Zoom: {data['zoom']}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Add Client Count to Video Feed
            cv2.putText(frame, f"Clients: {len(connected_websockets)}", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # --- DISPLAY THE WINDOW ---
            cv2.imshow("Gesture Capture (Press 'q' to quit)", frame)
            
            # Required to update the window; check for 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit signal received.")
                break

            # Broadcast to clients
            if connected_websockets:
                message = json.dumps(data)
                for ws in list(connected_websockets):
                    try:
                        await ws.send_str(message)
                    except Exception:
                        connected_websockets.remove(ws)
                    
    except asyncio.CancelledError:
        print("Camera loop cancelled")
    finally:
        cap.release()
        cv2.destroyAllWindows()

# --- 3. App Setup ---
async def on_startup(app):
    app['camera_task'] = asyncio.create_task(capture_and_process(app))

async def on_cleanup(app):
    app['camera_task'].cancel()
    await app['camera_task']

async def init_app():
    app = web.Application()
    app.router.add_get('/', lambda r: web.FileResponse('./static/index.html'))
    app.router.add_get('/ws', websocket_handler)
    app.router.add_static('/static/', path='./static', name='static')
    
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    return app

if __name__ == '__main__':
    print("======== Running on http://0.0.0.0:8080 ========")
    web.run_app(init_app(), host='0.0.0.0', port=8080)