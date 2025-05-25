import cv2
import time
import face_recognition


async def capture_face():
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)

        for top, right, bottom, left in face_locations:
            cor = (0, 255, 0) if len(face_locations) == 1 else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)

        if len(face_locations) > 1:
            cv2.putText(
                frame,
                "Apenas uma pessoa!",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        elif len(face_locations) == 0:
            cv2.putText(
                frame,
                "Nenhum rosto detectado",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
        else:
            elapsed = time.time() - start_time
            cv2.putText(
                frame,
                f"Capturando em {max(0, int(4 - elapsed))}s...",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if len(face_locations) == 1 and time.time() - start_time > 4:
            encoding = face_recognition.face_encodings(rgb, face_locations)[0]
            cap.release()
            cv2.destroyAllWindows()
            return encoding

        if len(face_locations) != 1:
            start_time = time.time()
    cap.release()
    cv2.destroyAllWindows()
    return None
