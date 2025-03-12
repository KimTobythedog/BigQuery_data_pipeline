from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import storage
import os

app = Flask(__name__)
app.secret_key = 
# Replace with a real secret key

# Replace with your actual GCS bucket name
GCS_BUCKET = 'GCS_BUKET_NAME_INSERT'
PROJECT_ID = 'PROJECT_ID_INSERT'

# Initialize a Cloud Storage client
storage_client = storage.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the request has a file part
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # If no file is selected, browser also submits an empty part without filename
    if file.filename == '':
        flash('No file selected for uploading.')
        return redirect(url_for('index'))
    
    try:
        # Access your GCS bucket and create a new blob with the uploaded file's name
        bucket = storage_client.get_bucket(GCS_BUCKET)
        blob = bucket.blob(file.filename)
        
        # Upload the file to GCS
        blob.upload_from_file(file)
        
        flash('File successfully uploaded to GCS.')
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
