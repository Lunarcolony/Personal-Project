# DNA Sequencing Analysis Platform

A professional web-based application for DNA sequence analysis with AI-powered predictions and comprehensive visualization capabilities.

## Features

### 🧬 Core Functionality
- **DNA Sequence Analysis**: Comprehensive analysis of DNA sequences including:
  - Nucleotide composition (A, T, G, C counts)
  - GC content calculation
  - Molecular weight determination
  - Sequence length and statistics

### 🤖 AI-Powered Analysis
- **Pretrained Model Integration**: Simulated AI model for:
  - Quality score prediction
  - Feature detection (promoters, coding sequences, terminators)
  - Variant calling (SNPs)
  - Confidence scoring

### 📊 Advanced Visualizations
- **Signal Chromatogram**: Visual representation of DNA sequencing signals
- **Nucleotide Composition Chart**: Bar chart showing base distribution
- **GC Content Distribution**: Sliding window analysis of GC content
- **GC Skew Analysis**: GC skew plot for replication origin detection

### 🔬 Detailed Analysis
- **Open Reading Frames (ORFs)**: Automatic detection of potential coding regions
- **Sequence Translation**: DNA to RNA transcription and protein translation
- **Complementary Sequences**: Calculate complement and reverse complement
- **Multi-frame Analysis**: Support for all reading frames

### 💻 User Interface
- **Professional Design**: Modern, responsive web interface
- **Dual Input Methods**: 
  - Text input for pasting sequences
  - File upload for FASTA/FASTQ files
- **Example Sequences**: Pre-loaded examples for testing
- **Export Options**: Download results in JSON, TXT, or CSV format

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**:
```bash
git clone https://github.com/Lunarcolony/Personal-Project.git
cd Personal-Project
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Access the application**:
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Text Input Method
1. Click on the "Text Input" tab
2. Paste your DNA sequence (FASTA format or raw sequence)
3. Or click on one of the example buttons to load a sample sequence
4. Click "Analyze Sequence" button
5. View comprehensive results including visualizations and statistics

### File Upload Method
1. Click on the "File Upload" tab
2. Click the upload area or drag and drop a file
3. Supported formats: .fasta, .fa, .fastq, .fq, .txt, .seq
4. Click "Upload & Analyze" button
5. View analysis results

### Understanding Results

#### AI Predictions
- **Quality Score**: Overall sequence quality (85-99%)
- **Confidence**: Model confidence in predictions (80-95%)
- **Predicted Features**: Potential biological features with probability scores
- **Variant Calls**: Detected sequence variants (SNPs)

#### Statistics
- **Sequence Length**: Total number of base pairs
- **GC Content**: Percentage of G and C nucleotides
- **Nucleotide Counts**: Individual counts for A, T, G, C
- **Molecular Weight**: Calculated molecular weight in Daltons

#### Visualizations
- **Chromatogram**: Simulated sequencing signal for each nucleotide
- **Composition**: Bar chart of nucleotide distribution
- **GC Distribution**: GC content across the sequence
- **GC Skew**: (G-C)/(G+C) ratio useful for origin detection

#### Detailed Analysis
- **Sequence Details**: Original, complement, and reverse complement
- **ORFs**: Open reading frames with start/end positions
- **Translation**: RNA transcription and protein translation

### Exporting Results
Click on any export button to download results:
- **JSON**: Full structured data
- **TXT**: Human-readable report
- **CSV**: Spreadsheet-compatible format

## Technical Details

### Technologies Used
- **Backend**: Flask (Python web framework)
- **Bioinformatics**: Biopython for sequence analysis
- **Data Processing**: NumPy, Pandas
- **Visualization**: Matplotlib
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design patterns

### API Endpoints

#### POST /api/analyze
Analyze DNA sequence from text input
```json
{
  "sequence": "ATGCGATCG..."
}
```

#### POST /api/upload
Upload and analyze DNA sequence file
- Accepts multipart/form-data with file

#### POST /api/predict
Get AI model predictions for sequence
```json
{
  "sequence": "ATGCGATCG..."
}
```

### File Structure
```
Personal-Project/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   ├── js/
│   │   └── main.js       # Frontend JavaScript
│   └── generated/        # Generated visualizations
└── uploads/              # Temporary file uploads
```

## Security Considerations
- File size limit: 16MB
- Allowed file extensions validated
- Temporary files automatically cleaned up
- No persistent storage of user data

## Future Enhancements
- Integration with real pretrained models (DeepVariant, etc.)
- Support for more sequence formats
- Batch processing capabilities
- Database storage for analysis history
- User authentication and profiles
- Advanced variant annotation
- Phylogenetic analysis tools
- Multiple sequence alignment

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License
This project is open source and available for educational and research purposes.

## Contact
For questions or support, please open an issue in the repository.

---
Built with ❤️ for bioinformatics research and education
