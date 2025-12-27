from flask import Flask, request, render_template, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pandas as pd
from utils.image_processor import extract_table_from_image
from utils.chart_detector import detect_chart_type, extract_data_from_chart
from utils.visual_generator import generate_visualizations
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-table')
def upload_table_page():
    return render_template('upload_image.html')

@app.route('/upload-chart')
def upload_chart_page():
    return render_template('upload_chart.html')

@app.route('/process-table', methods=['POST'])
def process_table():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Use PNG, JPG, or PDF'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract table data from image
        df = extract_table_from_image(filepath)
        
        if df is None or df.empty:
            return jsonify({'error': 'Could not extract data from image'}), 400
        
        # Generate visualizations
        charts = generate_visualizations(df, timestamp)
        
        # Prepare response
        response = {
            'success': True,
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'charts': charts,
            'table_html': df.to_html(classes='table table-striped', index=False)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process-chart', methods=['POST'])
def process_chart():
    try:
        if 'chart' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['chart']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Use PNG, JPG, or PDF'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect chart type
        chart_type = detect_chart_type(filepath)
        
        # Extract data from chart
        df = extract_data_from_chart(filepath, chart_type)
        
        if df is None or df.empty:
            return jsonify({'error': 'Could not extract data from chart'}), 400
        
        # Save as CSV
        csv_filename = f"{timestamp}_extracted_data.csv"
        csv_path = os.path.join(app.config['OUTPUT_FOLDER'], csv_filename)
        df.to_csv(csv_path, index=False)
        
        response = {
            'success': True,
            'chart_type': chart_type,
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'table_html': df.to_html(classes='table table-striped', index=False),
            'csv_file': csv_filename
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001
            )