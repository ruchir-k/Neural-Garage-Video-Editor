import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist

def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
    B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)

    # return the mouth aspect ratio
    return mar

cap = cv2.VideoCapture(0)

hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

MOUTH_AR_THRESH = 0.5
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

while True:
    success, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
        face_landmarks = face_utils.shape_to_np(face_landmarks)

        mouth = face_landmarks[mStart:mEnd]

        mouthMAR = mouth_aspect_ratio(mouth)
        mar = mouthMAR

        mouthHull = cv2.convexHull(mouth)

        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw text if mouth is open
        if mar > MOUTH_AR_THRESH:
            cv2.putText(frame, "Mouth is Open!", (30,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

        cv2.imshow("Face Landmarks", frame)
        cv2.waitKey(1)

