import cv2
import time
import asyncio
import face_recognition
from backend.message import say

async def capture_face():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return None

    init_time = time.time()
    startup_delay = 2
    warned_multiple_faces = False
    last_warning_time = 0
    single_face_start_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        current_time = time.time()
        if current_time - init_time < startup_delay:
            continue

        if len(face_locations) > 1:
            single_face_start_time = None
            if not warned_multiple_faces or (current_time - last_warning_time > 5):
                warned_multiple_faces = True
                last_warning_time = current_time
                await say("Somente uma pessoa deve estar visível na tela")
            continue

        if len(face_locations) == 0:
            single_face_start_time = None
            warned_multiple_faces = False
            continue

        if len(face_locations) == 1:
            warned_multiple_faces = False
            if single_face_start_time is None:
                single_face_start_time = current_time

            elif current_time - single_face_start_time >= 5:
                encodings = face_recognition.face_encodings(rgb, face_locations)
                if encodings:
                    encoding = encodings[0]
                    await asyncio.sleep(1)
                    cap.release()
                    cv2.destroyAllWindows()
                    return encoding

    cap.release()
    cv2.destroyAllWindows()
    return None