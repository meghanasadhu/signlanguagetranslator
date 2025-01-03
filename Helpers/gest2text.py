import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import mediapipe as mp
from tensorflow.keras.models import Sequential,load_model
import tensorflow as tf

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                              mp_drawing.DrawingSpec(
                                  color=(80, 110, 10), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(
                                  color=(80, 256, 121), thickness=1, circle_radius=1)
                              )
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(
                                  color=(80, 44, 121), thickness=2, circle_radius=2)
                              )
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(
                                  color=(121, 44, 250), thickness=2, circle_radius=2)
                              )
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(
                                  color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(
                                  color=(245, 66, 230), thickness=2, circle_radius=2)
                              )


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten(
    ) if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten(
    ) if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten(
    ) if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten(
    ) if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    return output_frame


def convert(flag):

    sequence = []
    sentence = []
    predictions = []
    threshold = 0.3
    print('debug')
    #frameRate = cap.get(5)
    # ISL Continents and Countries/Mali.mp4
    if(flag):
        ls = ['0 zero',
              '1 one',
              '1,00,00,000 one crore',
              '1,00,000 one lakh',
              '1,000 thousand',
              '10 ten',
              '10,000 ten thousand',
              '100 hundred',
              '11 eleven',
              '12 twelve',
              '13 thirteen',
              '14 fourteen',
              '15 fifteen',
              '16 sixteen',
              '17 seventeen',
              '18 eighteen',
              '19 nineteen',
              '2 two',
              '2,000 two thousand',
              '20 twenty',
              '21 twenty one',
              '3 three',
              '30 thirty',
              '4 four',
              '5 five',
              '50 fifty',
              '500 five hundred',
              '6 six',
              '60 sixty',
              '7 seven',
              '70 seventy',
              '8 eight',
              '9 nine',
              'Afghanistan',
              'Africa ',
              'Africa',
              'Antarctica',
              'Argentina',
              'Armenia',
              'Cambodia',
              'Canada',
              'Chile',
              'China',
              'Costa Rica',
              'Croatia',
              'Cyprus',
              'Czech Republic',
              'Denmark',
              'Egypt ',
              'Egypt',
              'El Salvador',
              'England ',
              'Kazakhstan',
              'Kenya',
              'Korea',
              'Kuwait',
              'Maharashtra',
              'Mali',
              'Numbers (0-1 crore)'
              ]
        actions = np.array(ls)
        model = load_model('./Signlang_Countries/model_upload.h5')
        model.load_weights('./Signlang_Countries/model_upload.h5')
        colors = []
        for i in actions:
            colors.append((245, 117, 16))
        cap = cv2.VideoCapture('./static/uploaded/video.mp4')
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if(ret == True):
                    image, results = mediapipe_detection(frame, holistic)
                if not (results.left_hand_landmarks or results.right_hand_landmarks):
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    continue
                draw_styled_landmarks(image, results)
                keypoints = extract_keypoints(results)
                sequence.append(keypoints)
                sequence = sequence[-30:]
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    #print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))
                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:

                            if len(sentence) > 0:
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])
                    if len(sentence) > 3:
                        sentence = sentence[-3:]
                cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
                cv2.putText(image, ' '.join(sentence), (3, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                # cv2.imshow('OpenCV Feed', image)
                if 0xFF == ord('q'):
                    break

                ret, buffer = cv2.imencode('.jpg', image)
                image = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
    
    else:
        ls = ['absent',
              'day',
              'Good morning',
              'Green',
              'hearing',
              'How are you',
              "I don't understand",
              'maths',
              'Maximum',
              'sign',
              'Take a photo',
              'Talk',
              'Thank you ver much',
              'time',
              'up']
        actions = np.array(ls)
        model = load_model('./Signlang_Realtime/sc_model_15_88A.h5')
        model.load_weights('./Signlang_Realtime/sc_model_15_88A.h5')
        colors = []
        for i in actions:
            colors.append((245, 117, 16))
        cap = cv2.VideoCapture(0)
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if(ret == True):
                    image, results = mediapipe_detection(frame, holistic)
                if not (results.left_hand_landmarks or results.right_hand_landmarks):
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    continue
                draw_styled_landmarks(image, results)
                keypoints = extract_keypoints(results)
                sequence.append(keypoints)
                sequence = sequence[-20:]
                if len(sequence) == 20:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))
                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:

                            if len(sentence) > 0:
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])
                    if len(sentence) > 3:
                        sentence = sentence[-3:]
                cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
                cv2.putText(image, ' '.join(sentence), (3, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                # cv2.imshow('OpenCV Feed', image)
                if 0xFF == ord('q'):
                    break

                ret, buffer = cv2.imencode('.jpg', image)
                image = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
