import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
# moviepy packaged with this environment exposes utilities at the top level
from moviepy import VideoFileClip, concatenate_videoclips

UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER
app.secret_key = 'replace-this-with-a-random-secret'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', merged_url=None)


@app.route('/merge', methods=['POST'])
def merge_videos():
    if 'videos' not in request.files:
        flash('No videos part in the request')
        return redirect(url_for('index'))

    files = request.files.getlist('videos')
    clips = []
    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filenames.append(filepath)
            clips.append(VideoFileClip(filepath))
    if len(clips) < 2:
        flash('Please upload at least two valid video files.')
        return redirect(url_for('index'))

    merged_clip = concatenate_videoclips(clips, method='compose')
    merged_filename = 'merged.mp4'
    merged_path = os.path.join(app.config['MERGED_FOLDER'], merged_filename)
    merged_clip.write_videofile(merged_path, codec='libx264', audio_codec='aac')
    merged_clip.close()
    for clip in clips:
        clip.close()
    # Optionally remove uploaded files
    for path in filenames:
        os.remove(path)
    return render_template('index.html', merged_url=url_for('download_file', filename=merged_filename))


@app.route('/merged/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['MERGED_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
