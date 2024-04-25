from flask import Flask, render_template, request, send_file
from docx import Document
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_transcript():
    youtube_video = request.form['video_url']
    video_id = youtube_video.split('=')[-1]
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = ""
        for i in transcript:
            result += ' ' + i['text']
        
        if result:
            doc = Document()
            doc.add_paragraph(result)
            doc.save('transcript.docx')
            return send_file('transcript.docx', as_attachment=True)
        else:
            return "Transcript not available for this video."
    
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
