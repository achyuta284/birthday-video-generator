from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import random
from moviepy.editor import ImageSequenceClip, AudioFileClip, TextClip, CompositeVideoClip

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/videos"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-video", methods=["POST"])
def generate_video():
    images = request.files.getlist("images")
    music = request.files.get("music")
    message = request.form.get("message", "")
    format_type = request.form.get("format")
    quality = request.form.get("quality")
    duration = int(request.form.get("duration"))

    image_paths = []
    for image in images:
        path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(path)
        image_paths.append(path)

    if not image_paths:
        return jsonify({"success": False, "error": "No images uploaded!"})

    # Set video size based on format
    video_width, video_height = (1280, 720) if format_type == "landscape" else (720, 1280)

    fps = 24
    clip = ImageSequenceClip(image_paths, fps=fps)
    clip = clip.set_duration(duration)

    # Add music if uploaded
    if music:
        music_path = os.path.join(UPLOAD_FOLDER, music.filename)
        music.save(music_path)
        audio = AudioFileClip(music_path)
        clip = clip.set_audio(audio)

    # Add custom message as text overlay
    if message:
        text_clip = TextClip(message, fontsize=50, color='white', size=(video_width, None), method="caption")
        text_clip = text_clip.set_position(("center", "bottom")).set_duration(duration)
        clip = CompositeVideoClip([clip, text_clip])

    # Generate unique video filename
    video_filename = f"video_{random.randint(1000, 9999)}.mp4"
    video_path = os.path.join(OUTPUT_FOLDER, video_filename)

    # Save video
    clip.write_videofile(video_path, codec="libx264", fps=fps)

    return jsonify({"success": True, "video_url": f"/static/videos/{video_filename}"})

@app.route("/static/videos/<filename>")
def get_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
