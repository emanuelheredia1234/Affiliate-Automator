# Video Merger Web App

This simple Flask application allows you to upload multiple video files and merge them into a single video. It uses `moviepy` under the hood.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Open your browser at [http://localhost:5000](http://localhost:5000) to use the interface.

Merged videos are temporarily stored in the `merged/` directory and offered for download after processing.
