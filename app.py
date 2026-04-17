from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        format_type = request.form.get("format")

        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }

        if format_type == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            })
        else:
            ydl_opts.update({'format': 'best'})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if format_type == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        return send_file(filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
