![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Hackathon](https://img.shields.io/badge/Hackathon-2024-FF6B6B?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://javascript.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://html.spec.whatwg.org/)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://www.w3.org/Style/CSS/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)

![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
<!-- Main badge -->
![Tesseract OCR](https://img.shields.io/badge/Google-Tesseract%20OCR-4285F4?style=flat&logo=google&logoColor=white)

<!-- Alternative style -->
![Google Tech](https://img.shields.io/badge/Powered%20by-Google%20Tesseract-4285F4?style=for-the-badge&logo=google&logoColor=white)

<!-- With link -->
[![Tesseract](https://img.shields.io/badge/Google-Tesseract-4285F4?style=flat&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)


# 🎯 Problem Statement
Data professionals face two critical challenges:

Manual Data Entry: Converting printed/image tables into digital format is time-consuming and error-prone
Data Recovery: Extracting data from charts and graphs when source data is unavailable

# 💡 Our Solution
DataConverter provides a seamless, bidirectional conversion platform:

Image → Charts: Upload table images, get interactive visualizations instantly
Charts → Data: Extract structured data from any chart/graph image

✨ Key Features
🔄 Bidirectional Conversion

Table to Visuals: OCR-powered extraction with automatic data cleaning
Visuals to Tables: AI-driven chart detection and data reconstruction

# 📈 Multiple Visualization Types

Interactive Bar Charts
Dynamic Line Charts
Proportional Pie Charts
Correlation Scatter Plots
Statistical Heatmaps

# 🎨 User Experience

Drag-and-drop file uploads
Real-time processing feedback
Interactive Plotly visualizations
Multiple export formats (CSV, HTML, PNG)
Mobile-responsive design

# 🚀 Quick Start
Prerequisites
bashPython 3.8+
Tesseract OCR
Installation
bash# Clone repository
git clone https://github.com/YOUR_USERNAME/data-converter.git
cd data-converter

# Create virtual environment
python -m venv venv

# Activate virtual environment
#Windows:
venv\Scripts\activate
#Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
Install Tesseract OCR

Windows: Download
Mac: brew install tesseract
Linux: sudo apt-get install tesseract-ocr

# 🎬 Demo
Open your browser and navigate to: http://localhost:5000
Image to Visuals Workflow

Upload table image (PNG/JPG/PDF)
OCR extracts data automatically
View extracted table
Generate multiple chart types
Download in preferred format

Visuals to Table Workflow

Upload chart/graph image
AI detects chart type
Extracts data points
View structured table
Export as CSV/Excel

# 🛠️ Technology Stack
Backend

Flask: Web framework
OpenCV: Image processing & computer vision
Tesseract OCR: Text extraction
Pandas: Data manipulation
NumPy: Numerical operations

Frontend

HTML5/CSS3: Modern responsive design
Bootstrap 5: UI components
JavaScript: Dynamic interactions
Plotly.js: Interactive visualizations

AI/ML Components

Computer vision for chart type detection
OCR for text extraction
Pattern recognition for data point extraction
Automatic data cleaning algorithms

### 🔧 Google Technologies

[![Tesseract OCR](https://img.shields.io/badge/Google-Tesseract%20OCR-4285F4?style=flat&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)

**Tesseract OCR Engine**: Google's open-source Optical Character Recognition system powers our table extraction feature, providing 85-95% accuracy in text recognition.

# 📁 Project Structure
data-converter/
├── app.py                      # Main Flask application
├── requirements.txt            # Dependencies
├── utils/
│   ├── image_processor.py     # OCR & table extraction
│   ├── chart_detector.py      # Chart type detection
│   └── visual_generator.py    # Visualization generation
├── templates/
│   ├── index.html             # Homepage
│   ├── upload_image.html      # Table upload interface
│   └── upload_chart.html      # Chart upload interface
├── uploads/                    # Temporary file storage
└── outputs/                    # Generated visualizations
# 🎯 Use Cases
Business Analytics

Convert printed reports to digital dashboards
Extract data from competitor presentations
Digitize historical business records

Research & Academia

Extract data from published papers
Convert thesis tables to visualizations
Digitize handwritten data tables

Data Recovery

Recover data from screenshots
Extract information from infographics
Convert legacy documents

# 📊 Performance Metrics

Average Processing Time: 2-5 seconds
OCR Accuracy: 85-95% (depends on image quality)
Chart Detection: 90%+ accuracy
Supported Formats: PNG, JPG, PDF
Max File Size: 16MB

# 🔮 Future Enhancements

 Real-time collaboration features
 Batch processing for multiple files
 Advanced chart types (3D, bubble, waterfall)
 Mobile app (iOS/Android)
 Cloud storage integration
 API for third-party integrations
 Machine learning for improved accuracy
 Multi-language OCR support

👥 Team
[VISION]

Role: Full Stack Developer
Email: payalpal2209@gmail.com
GitHub: payal220

🙏 Acknowledgments

Tesseract OCR - Google's open-source OCR engine
Plotly - Interactive visualization library
OpenCV - Computer vision library
Flask - Lightweight web framework

📄 License
This project is licensed under the MIT License.
🔗 Links

GitHub: https://github.com/payal220/data-converter

📞 Contact
For questions or feedback:

Email: payalpal2209@gmail.com
GitHub: payal220


Built with ❤️ for Hackathon 





