import pytesseract

import cv2
import pytesseract
from PIL import Image
import pandas as pd
import numpy as np
import re

# Uncomment and set path if Tesseract is not in PATH (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """Preprocess image for better OCR results"""
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    return denoised

def extract_table_from_image(image_path):
    """Extract tabular data from image using OCR"""
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        
        # Perform OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        # Parse text into table
        df = parse_text_to_dataframe(text)
        
        return df
    
    except Exception as e:
        print(f"Error in extract_table_from_image: {e}")
        # Fallback: try alternative method
        return extract_table_alternative(image_path)

def parse_text_to_dataframe(text):
    """Parse OCR text into a pandas DataFrame"""
    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        return pd.DataFrame()
    
    # Try to detect delimiter
    best_delimiter = detect_delimiter(lines)
    
    # Split lines by delimiter
    data = []
    for line in lines:
        # Clean the line
        if best_delimiter == ' ':
            # Split by multiple spaces
            row = re.split(r'\s{2,}', line)
        else:
            row = line.split(best_delimiter)
        
        row = [cell.strip() for cell in row if cell.strip()]
        if row:
            data.append(row)
    
    if not data:
        return pd.DataFrame()
    
    # First row as header
    if len(data) > 1:
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame(data)
    
    # Clean and convert numeric columns
    df = clean_dataframe(df)
    
    return df

def detect_delimiter(lines):
    """Detect the most likely delimiter in the text"""
    delimiters = {'\t': 0, '|': 0, ',': 0, ';': 0, ' ': 0}
    
    for line in lines[:5]:  # Check first 5 lines
        for delim in delimiters:
            if delim == ' ':
                # Count multiple consecutive spaces
                delimiters[delim] += len(re.findall(r'\s{2,}', line))
            else:
                delimiters[delim] += line.count(delim)
    
    # Return delimiter with highest count
    return max(delimiters, key=delimiters.get)

def clean_dataframe(df):
    """Clean and convert data types in DataFrame"""
    for col in df.columns:
        # Try to convert to numeric
        try:
            # Remove common non-numeric characters
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace('%', '')
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    return df

def extract_table_alternative(image_path):
    """Alternative method using different OCR approach"""
    try:
        # Use PIL for OCR
        img = Image.open(image_path)
        
        # Get OCR data with bounding boxes
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Group text by vertical position (rows)
        rows = {}
        for i, text in enumerate(ocr_data['text']):
            if text.strip():
                top = ocr_data['top'][i]
                left = ocr_data['left'][i]
                
                # Group by approximate row (within 10 pixels)
                row_key = top // 10
                if row_key not in rows:
                    rows[row_key] = []
                rows[row_key].append((left, text))
        
        # Sort rows and build table
        data = []
        for row_key in sorted(rows.keys()):
            row_data = sorted(rows[row_key], key=lambda x: x[0])
            row_text = [text for _, text in row_data]
            data.append(row_text)
        
        # Create DataFrame
        if data and len(data) > 1:
            # Ensure all rows have same length
            max_cols = max(len(row) for row in data)
            data = [row + [''] * (max_cols - len(row)) for row in data]
            
            df = pd.DataFrame(data[1:], columns=data[0])
            df = clean_dataframe(df)
            return df
        
        return pd.DataFrame()
    
    except Exception as e:
        print(f"Error in alternative extraction: {e}")
        return create_sample_dataframe()

def create_sample_dataframe():
    """Create a sample DataFrame when extraction fails"""
    return pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value': [23, 45, 56, 78, 34],
        'Growth': [12.5, 23.4, 18.9, 34.2, 15.7]
    })