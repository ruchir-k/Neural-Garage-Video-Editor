from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

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
        # Process the video or redirect to a success page
        return render_template("upload_success.html", filename=video.filename)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
