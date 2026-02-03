# Quick Start Guide

## Running the Application

### Local Development

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Server**:
```bash
# For development (with debug mode)
FLASK_DEBUG=true python app.py

# For production (without debug mode)
python app.py
```

3. **Access the Application**:
Open your browser and go to: `http://localhost:5000`

## Using the Platform

### Option 1: Text Input

1. Navigate to the "Text Input" tab (default)
2. Paste your DNA sequence in the text area
   - Supports FASTA format with headers (>Header)
   - Supports raw DNA sequences (ATGC)
3. Or click one of the example buttons to load sample data:
   - **Short sequence**: ~44 bp
   - **Medium sequence**: ~1.8 kb
   - **Long sequence**: ~2.5 kb
4. Click "Analyze Sequence"
5. View comprehensive results including:
   - AI predictions
   - Sequence statistics
   - Signal chromatogram
   - Multiple visualizations
   - Detailed analysis

### Option 2: File Upload

1. Navigate to the "File Upload" tab
2. Click the upload area or drag and drop a file
3. Supported formats:
   - `.fasta`, `.fa` - FASTA format
   - `.fastq`, `.fq` - FASTQ format
   - `.txt` - Plain text DNA sequence
4. Click "Upload & Analyze"
5. View the same comprehensive results

## Understanding the Results

### AI Model Predictions
- **Quality Score**: Confidence in sequence accuracy (85-99%)
- **Analysis Confidence**: Model confidence (80-95%)
- **Predicted Features**: Biological features like promoters, coding sequences
- **Variant Calls**: Detected SNPs (when applicable)

### Sequence Statistics
- **Length**: Total base pairs
- **GC Content**: Percentage of G and C nucleotides (important for stability)
- **Nucleotide Counts**: Individual A, T, G, C counts
- **Molecular Weight**: Calculated in Daltons
- **ORFs Found**: Number of open reading frames detected

### Visualizations

1. **Signal Chromatogram**
   - Simulated sequencing signal for each nucleotide
   - Shows peaks for A (red), T (cyan), G (yellow), C (green)
   - Useful for quality assessment

2. **Nucleotide Composition**
   - Bar chart showing distribution of bases
   - Helps identify sequence bias

3. **GC Content Distribution**
   - Sliding window analysis across the sequence
   - Red dashed line shows average GC content
   - Useful for identifying regions with different composition

4. **GC Skew Analysis**
   - (G-C)/(G+C) ratio plot
   - Helps identify replication origins
   - Positive values indicate G-rich regions

### Detailed Analysis Tabs

**Sequence Details**:
- Original sequence (color-coded by base)
- Complement sequence
- Reverse complement sequence

**Open Reading Frames**:
- Table of ORFs found (minimum 75 bp)
- Shows start/end positions, length, frame, and strand
- Preview of sequence for each ORF

**Translation**:
- RNA transcription (DNA → RNA)
- Protein translation (RNA → protein)
- Includes stop codons (*)

## Exporting Results

Click any export button to download:
- **JSON**: Full structured data for programmatic use
- **TXT**: Human-readable report
- **CSV**: Statistics in spreadsheet format

## Example Workflows

### Basic Sequence Analysis
1. Load medium example sequence
2. Click "Analyze Sequence"
3. Review statistics and GC content
4. Check for ORFs in the "Open Reading Frames" tab
5. Export results as needed

### Quality Assessment
1. Upload your sequencing file
2. Check the AI Quality Score (should be >85%)
3. Review the chromatogram for signal quality
4. Look at GC distribution for consistency

### Gene Discovery
1. Input or upload DNA sequence
2. Check "Predicted Features" for coding sequences
3. Review "Open Reading Frames" tab
4. Look at "Translation" for potential proteins

## Tips and Best Practices

- **Sequence Length**: Works best with sequences from 50 bp to several kb
- **File Format**: Use FASTA format for best results
- **Example Data**: Test with examples before uploading your own data
- **Browser**: Use modern browsers (Chrome, Firefox, Safari, Edge)
- **Large Files**: Files over 16MB will be rejected for performance
- **Multiple Sequences**: Upload files with one sequence at a time

## Troubleshooting

### Common Issues

**Error: "No sequence provided"**
- Make sure you've entered or uploaded a sequence
- Check that the sequence contains valid DNA bases (ATGC)

**Error: "Invalid sequence format"**
- Remove any invalid characters
- Only A, T, G, C, and N are accepted

**Error: "Could not extract DNA sequence from file"**
- Check file format (should be FASTA, FASTQ, or plain text)
- Make sure file contains DNA sequences

**Visualizations not showing**
- Refresh the page and try again
- Check browser console for errors

**Slow analysis**
- Large sequences (>5kb) may take a few seconds
- Wait for the loading indicator to disappear

## Advanced Features

### Understanding AI Predictions

The platform uses simulated AI predictions. In a production environment, this could be replaced with:
- **DeepVariant**: For variant calling
- **Gene prediction models**: For feature detection
- **Quality assessment models**: For sequencing quality

### Custom Analysis

The backend API can be accessed directly:

```bash
# Analyze sequence
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"sequence": "ATGCGATCG..."}'

# Get predictions
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sequence": "ATGCGATCG..."}'
```

## Support

For issues or questions:
1. Check this guide
2. Review the main README.md
3. Open an issue on GitHub

## Security Notes

- Files are temporarily stored and automatically deleted
- No user data is persistently saved
- Debug mode is disabled by default
- File size and type restrictions are enforced
