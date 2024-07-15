import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist
from moviepy.editor import VideoFileClip

class FaceLandmarkDetector:
    def __init__(self, input_video_path, output_video_path, final_output_path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.final_output_path = final_output_path
        self.cap = cv2.VideoCapture(self.input_video_path)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.out = cv2.VideoWriter(self.output_video_path, cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.frame_width, self.frame_height))
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.MOUTH_AR_THRESH = 0.5
        (self.mStart, self.mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    def mouth_aspect_ratio(self, mouth):
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[4], mouth[8])
        C = dist.euclidean(mouth[0], mouth[6])
        mar = (A + B) / (2.0 * C)
        return mar

    def process_video(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.hog_face_detector(gray)
            for face in faces:
                face_landmarks = self.dlib_facelandmark(gray, face)
                face_landmarks = face_utils.shape_to_np(face_landmarks)

                mouth = face_landmarks[self.mStart:self.mEnd]
                mar = self.mouth_aspect_ratio(mouth)
                mouthHull = cv2.convexHull(mouth)

                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if mar > self.MOUTH_AR_THRESH:
                    cv2.putText(frame, "Mouth is Open!", (30,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

            self.out.write(frame)

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

        # Load the original and processed videos
        original_clip = VideoFileClip(self.input_video_path)
        processed_clip = VideoFileClip(self.output_video_path)

        # Set the audio of the processed clip to be the audio of the original clip
        processed_clip_with_audio = processed_clip.set_audio(original_clip.audio)

        # Write the result to a new file
        processed_clip_with_audio.write_videofile(self.final_output_path, codec="libx264", audio_codec="aac")

# Example usage
# if __name__ == "__main__":
#     input_video_path = "uploads/input_video.mp4"
#     processed_video_path = "processed/output.mp4"
#     final_output_path = "processed/final_output_with_audio.mp4"
#
#     # Process the video to detect facial landmarks
#     detector = FaceLandmarkDetector(input_video_path, processed_video_path, final_output_path)
#     detector.process_video()

