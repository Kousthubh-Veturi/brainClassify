# BrainClassify

A web application for brain tumor classification using MRI scans and AI.

## Features

- Upload MRI scan images for analysis
- Real-time classification of brain tumors into different categories
- Detailed analysis results with confidence scores
- Feedback system for continuous improvement
- Mobile-friendly, responsive interface

## Tech Stack

### Frontend
- React
- TailwindCSS
- Axios for API communication
- React Dropzone for file uploads
- React Router for navigation

### Backend
- FastAPI (Python)
- TensorFlow for AI model
- Local file storage for images
- JSON-based feedback storage

## Installation

### Prerequisites
- Python 3.8+ 
- Node.js 14+
- npm 6+

### Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/brainClassify.git
cd brainClassify
```

2. Run the verification script to check if all files are in place:
```
./verify_setup.sh
```

3. Run the app using the provided script:
```
./run.sh
```

This script will:
- Create a Python virtual environment
- Install all required dependencies
- Start the backend server on port 8000
- Start the frontend server on port 3000
- Open the application in your default browser

### Alternative Setup (Separate Servers)

If you want to run the frontend and backend separately:

#### Backend
```
./start_backend.sh
```

#### Frontend
```
./start_frontend.sh
```

## Usage

1. Open your browser and go to http://localhost:3000
2. Upload an MRI scan image using the upload area
3. Wait for the analysis to complete
4. View the results and interpretation
5. Provide feedback on the prediction accuracy

## Troubleshooting

### Blank Screen Issues
If you encounter a blank screen in the browser:

1. Check the browser console for errors (F12 or right-click > Inspect > Console)
2. Verify that the backend server is running at http://localhost:8000
3. Try the following fixes:

**Frontend Issues:**
- Delete the `node_modules` folder and run `npm install` again
- Make sure your React version is compatible with your dependencies
- Verify Tailwind CSS is properly installed and configured

**Backend Issues:**
- Check if API endpoints are accessible at http://localhost:8000/docs
- Verify uploads directory exists and has proper permissions
- Check backend logs for any errors

## Project Structure

```
brainClassify/
├── backend/            # Python FastAPI backend
│   ├── app/
│   │   ├── main.py     # Main application file
│   │   ├── routes/     # API endpoints
│   │   └── services/   # Business logic
│   └── requirements.txt
│
├── frontend/           # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   └── services/   # API service
│   └── package.json
│
├── model/              # AI model files
│   ├── vit_model.py    # Vision Transformer model
│   └── train_vit.py    # Training script
│
├── uploads/            # Local storage for uploaded images
├── feedback/           # Local storage for user feedback
├── run.sh              # Startup script
├── start_frontend.sh   # Frontend startup script
├── start_backend.sh    # Backend startup script
├── verify_setup.sh     # Verification script
└── README.md           # This file
```

## Dataset Citation

This project uses the BraTS 2021 dataset. If you use this dataset, please cite:

[1] U.Baid, et al., The RSNA-ASNR-MICCAI BraTS 2021 Benchmark on Brain Tumor Segmentation and Radiogenomic Classification, arXiv:2107.02314, 2021.

[2] B. H. Menze, A. Jakab, S. Bauer, J. Kalpathy-Cramer, K. Farahani, J. Kirby, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)", IEEE Transactions on Medical Imaging 34(10), 1993-2024 (2015) DOI: 10.1109/TMI.2014.2377694

[3] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J.S. Kirby, et al., "Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features", Nature Scientific Data, 4:170117 (2017) DOI: 10.1038/sdata.2017.117

## License

MIT

## Disclaimer

This application is for educational purposes only and should not be used for medical diagnosis. Always consult with healthcare professionals for medical advice.
