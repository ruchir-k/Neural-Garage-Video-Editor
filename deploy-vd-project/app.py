from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
import os
from faceLandmark import FaceLandmarkDetector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'video' not in request.files:
        return redirect(request.url)

    video = request.files['video']

    if video.filename == '':
        return redirect(request.url)

    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_path)

        processed_video_path = os.path.join(app.config['PROCESSED_FOLDER'], "processed_" + video.filename)
        final_output_path = os.path.join(app.config['PROCESSED_FOLDER'], "final_" + video.filename)

        detector = FaceLandmarkDetector(video_path, processed_video_path, final_output_path)
        detector.process_video()

        return render_template("upload_success.html", filename=video.filename)

@app.route("/static/processed/<filename>")
def processed_file(filename):
    if not filename.endswith(".mp4"):
        abort(404)  # Only allow .mp4 files to be served

    video_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    if os.path.exists(video_path):
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True, mimetype='video/mp4')
    else:
        abort(404)  # File not found

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)
