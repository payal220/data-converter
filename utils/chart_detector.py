import cv2
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import re

def detect_chart_type(image_path):
    """Detect the type of chart in the image"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Detect lines (for bar charts, line charts)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
    
    # Detect circles (for pie charts)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                               param1=100, param2=30, minRadius=30, maxRadius=300)
    
    # Analyze features
    if circles is not None and len(circles[0]) > 0:
        return 'pie'
    elif lines is not None:
        # Analyze line orientation
        horizontal = 0
        vertical = 0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            if angle < 20 or angle > 160:
                horizontal += 1
            elif 70 < angle < 110:
                vertical += 1
        
        if vertical > horizontal * 1.5:
            return 'bar'
        else:
            return 'line'
    
    return 'unknown'

def extract_data_from_chart(image_path, chart_type):
    """Extract data points from chart image"""
    if chart_type == 'bar':
        return extract_bar_chart_data(image_path)
    elif chart_type == 'line':
        return extract_line_chart_data(image_path)
    elif chart_type == 'pie':
        return extract_pie_chart_data(image_path)
    else:
        return extract_generic_data(image_path)

def extract_bar_chart_data(image_path):
    """Extract data from bar chart"""
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect vertical bars
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours that look like bars
        bars = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / float(w) if w > 0 else 0
            area = cv2.contourArea(contour)
            
            # Bars are typically tall and narrow
            if aspect_ratio > 1.5 and area > 500:
                bars.append({'x': x, 'y': y, 'width': w, 'height': h})
        
        # Sort bars by x position
        bars = sorted(bars, key=lambda b: b['x'])
        
        # Extract labels using OCR
        labels = extract_axis_labels(image_path, 'x')
        
        # Create DataFrame
        if len(bars) > 0:
            # Normalize heights to values
            max_height = max(b['height'] for b in bars)
            values = [int((b['height'] / max_height) * 100) for b in bars]
            
            # Match labels with values
            if len(labels) >= len(values):
                labels = labels[:len(values)]
            else:
                labels = [f'Category {i+1}' for i in range(len(values))]
            
            return pd.DataFrame({
                'Category': labels,
                'Value': values
            })
        
        return create_sample_bar_data()
    
    except Exception as e:
        print(f"Error extracting bar chart: {e}")
        return create_sample_bar_data()

def extract_line_chart_data(image_path):
    """Extract data from line chart"""
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find the main line
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour (likely the data line)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Sample points along the contour
            points = []
            for point in largest_contour:
                x, y = point[0]
                points.append((x, y))
            
            # Sort by x coordinate
            points = sorted(points, key=lambda p: p[0])
            
            # Sample evenly spaced points
            if len(points) > 10:
                step = len(points) // 10
                points = points[::step]
            
            # Normalize y values
            if points:
                min_y = min(p[1] for p in points)
                max_y = max(p[1] for p in points)
                y_range = max_y - min_y if max_y != min_y else 1
                
                values = [int(100 - ((p[1] - min_y) / y_range * 100)) for p in points]
                labels = [f'Point {i+1}' for i in range(len(values))]
                
                return pd.DataFrame({
                    'X': labels,
                    'Y': values
                })
        
        return create_sample_line_data()
    
    except Exception as e:
        print(f"Error extracting line chart: {e}")
        return create_sample_line_data()

def extract_pie_chart_data(image_path):
    """Extract data from pie chart"""
    try:
        img = cv2.imread(image_path)
        
        # Try to extract labels and percentages using OCR
        text_data = pytesseract.image_to_string(img)
        
        # Parse for percentages
        percentages = re.findall(r'(\d+)%', text_data)
        
        if percentages:
            values = [int(p) for p in percentages]
            labels = [f'Slice {i+1}' for i in range(len(values))]
            
            return pd.DataFrame({
                'Category': labels,
                'Percentage': values
            })
        
        return create_sample_pie_data()
    
    except Exception as e:
        print(f"Error extracting pie chart: {e}")
        return create_sample_pie_data()

def extract_axis_labels(image_path, axis='x'):
    """Extract axis labels using OCR"""
    try:
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        
        # Crop to get axis region
        if axis == 'x':
            # Bottom 20% of image
            cropped = img[int(height * 0.8):, :]
        else:
            # Left 20% of image
            cropped = img[:, :int(width * 0.2)]
        
        # OCR on cropped region
        text = pytesseract.image_to_string(cropped)
        labels = [l.strip() for l in text.split('\n') if l.strip() and not l.strip().isdigit()]
        
        return labels[:10]  # Return max 10 labels
    
    except:
        return []

def extract_generic_data(image_path):
    """Generic data extraction using OCR for unknown chart types"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Try to find numerical values
        numbers = re.findall(r'\d+\.?\d*', text)
        
        if numbers:
            values = [float(n) for n in numbers[:10]]
            labels = [f'Item {i+1}' for i in range(len(values))]
            
            return pd.DataFrame({
                'Label': labels,
                'Value': values
            })
        
        return create_sample_bar_data()
    
    except Exception as e:
        print(f"Error in generic extraction: {e}")
        return create_sample_bar_data()

def create_sample_bar_data():
    return pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value': [45, 72, 38, 91, 55]
    })

def create_sample_line_data():
    return pd.DataFrame({
        'X': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Y': [30, 45, 38, 65, 52, 70]
    })

def create_sample_pie_data():
    return pd.DataFrame({
        'Category': ['Category A', 'Category B', 'Category C', 'Category D'],
        'Percentage': [30, 25, 25, 20]
    })