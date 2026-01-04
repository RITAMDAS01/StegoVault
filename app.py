import os
from flask import Flask, render_template, request, send_file, flash, redirect
from image_stego import hide_in_image, reveal_from_image
from audio_stego import hide_in_audio, reveal_from_audio
from text_stego import hide_text_in_text, reveal_text_from_text

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    action = request.form['action']
    file = request.files['file']
    message = request.form.get('message', '')
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    if action == 'hide':
        output_path = os.path.join(UPLOAD_FOLDER, 'stego_' + file.filename)
        hide_in_image(filepath, message, output_path)
        return send_file(output_path, as_attachment=True)
    else:
        result = reveal_from_image(filepath)
        flash(f"Decoded Message: {result}")
        return redirect('/')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    action = request.form['action']
    file = request.files['file']
    message = request.form.get('message', '')
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    if action == 'hide':
        output_path = os.path.join(UPLOAD_FOLDER, 'stego_' + file.filename)
        hide_in_audio(filepath, message, output_path)
        return send_file(output_path, as_attachment=True)
    else:
        result = reveal_from_audio(filepath)
        flash(f"Decoded Message: {result}")
        return redirect('/')

@app.route('/process_text', methods=['POST'])
def process_text():
    action = request.form['action']
    if action == 'hide':
        cover = request.form['cover_text']
        secret = request.form['secret_text']
        result = hide_text_in_text(cover, secret)
        flash(f"Copy this text: {result}")
    else:
        cover = request.form['cover_text']
        result = reveal_text_from_text(cover)
        flash(f"Hidden Message: {result}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)