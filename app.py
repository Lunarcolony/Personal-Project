from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction, molecular_weight
import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'fasta', 'fa', 'fastq', 'fq', 'txt', 'seq', 'ab1'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/generated', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_sequence(sequence_str):
    """Analyze a DNA sequence and return comprehensive statistics"""
    try:
        seq = Seq(sequence_str.upper())
        
        # Basic statistics
        length = len(seq)
        gc_content = gc_fraction(seq) * 100
        
        # Count nucleotides
        a_count = sequence_str.upper().count('A')
        t_count = sequence_str.upper().count('T')
        g_count = sequence_str.upper().count('G')
        c_count = sequence_str.upper().count('C')
        
        # Complement and reverse complement
        complement = str(seq.complement())
        reverse_complement = str(seq.reverse_complement())
        
        # Transcription (DNA to RNA)
        rna = str(seq.transcribe())
        
        # Translation (get protein sequence)
        try:
            protein = str(seq.translate(to_stop=False))
        except:
            protein = "Unable to translate"
        
        # Molecular weight
        try:
            mol_weight = molecular_weight(seq, seq_type='DNA')
        except:
            mol_weight = 0
        
        # Find ORFs (Open Reading Frames)
        orfs = find_orfs(sequence_str)
        
        # Calculate GC skew
        gc_skew = calculate_gc_skew(sequence_str)
        
        return {
            'length': length,
            'gc_content': round(gc_content, 2),
            'a_count': a_count,
            't_count': t_count,
            'g_count': g_count,
            'c_count': c_count,
            'complement': complement,
            'reverse_complement': reverse_complement,
            'rna': rna,
            'protein': protein,
            'molecular_weight': round(mol_weight, 2),
            'orfs': orfs,
            'gc_skew': gc_skew
        }
    except Exception as e:
        return {'error': str(e)}

def find_orfs(sequence, min_length=75):
    """Find Open Reading Frames in the sequence"""
    seq = Seq(sequence.upper())
    orfs = []
    
    # Look for ORFs in all 3 forward frames
    for frame in range(3):
        for i in range(frame, len(seq) - 2, 3):
            codon = seq[i:i+3]
            if str(codon) == 'ATG':  # Start codon
                for j in range(i + 3, len(seq) - 2, 3):
                    codon = seq[j:j+3]
                    if str(codon) in ['TAA', 'TAG', 'TGA']:  # Stop codons
                        orf_seq = seq[i:j+3]
                        if len(orf_seq) >= min_length:
                            orfs.append({
                                'start': i,
                                'end': j + 3,
                                'length': len(orf_seq),
                                'frame': frame + 1,
                                'strand': '+',
                                'sequence': str(orf_seq)
                            })
                        break
    
    return orfs[:10]  # Return top 10 ORFs

def calculate_gc_skew(sequence, window=100):
    """Calculate GC skew across the sequence"""
    skew_values = []
    positions = []
    
    for i in range(0, len(sequence) - window, window):
        window_seq = sequence[i:i+window].upper()
        g_count = window_seq.count('G')
        c_count = window_seq.count('C')
        
        if g_count + c_count > 0:
            skew = (g_count - c_count) / (g_count + c_count)
        else:
            skew = 0
        
        skew_values.append(skew)
        positions.append(i + window // 2)
    
    return {'positions': positions, 'values': skew_values}

def generate_sequence_visualization(sequence, analysis):
    """Generate various visualizations for the DNA sequence"""
    visualizations = {}
    
    # 1. Nucleotide composition bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    nucleotides = ['A', 'T', 'G', 'C']
    counts = [analysis['a_count'], analysis['t_count'], analysis['g_count'], analysis['c_count']]
    colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#6BCB77']
    
    ax.bar(nucleotides, counts, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Nucleotide', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Nucleotide Composition', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    visualizations['composition'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    # 2. GC content sliding window
    if len(sequence) > 50:
        window_size = max(50, len(sequence) // 50)
        positions = []
        gc_contents = []
        
        for i in range(0, len(sequence) - window_size, window_size // 2):
            window = sequence[i:i+window_size].upper()
            gc = (window.count('G') + window.count('C')) / len(window) * 100
            positions.append(i + window_size // 2)
            gc_contents.append(gc)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(positions, gc_contents, color='#6BCB77', linewidth=2)
        ax.axhline(y=analysis['gc_content'], color='red', linestyle='--', 
                   label=f'Average GC: {analysis["gc_content"]:.1f}%')
        ax.set_xlabel('Position (bp)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GC Content (%)', fontsize=12, fontweight='bold')
        ax.set_title('GC Content Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        visualizations['gc_distribution'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    # 3. GC Skew plot
    if analysis.get('gc_skew') and len(analysis['gc_skew']['positions']) > 0:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(analysis['gc_skew']['positions'], analysis['gc_skew']['values'], 
                color='#4ECDC4', linewidth=2)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_xlabel('Position (bp)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GC Skew', fontsize=12, fontweight='bold')
        ax.set_title('GC Skew Analysis', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        visualizations['gc_skew'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
    
    # 4. Signal chromatogram simulation (for visual appeal)
    fig, axes = plt.subplots(4, 1, figsize=(12, 6), sharex=True)
    colors_map = {'A': '#FF6B6B', 'T': '#4ECDC4', 'G': '#FFD93D', 'C': '#6BCB77'}
    nucleotide_list = ['A', 'T', 'G', 'C']
    
    # Simulate signal for first 100 bases
    display_length = min(100, len(sequence))
    x = np.arange(display_length)
    
    for idx, nuc in enumerate(nucleotide_list):
        # Generate simulated signal
        signal = np.zeros(display_length)
        for i, base in enumerate(sequence[:display_length].upper()):
            if base == nuc:
                # Create a peak at this position
                signal[i] = 1.0 + np.random.normal(0, 0.1)
            else:
                signal[i] = np.random.normal(0, 0.05)
        
        # Smooth the signal
        from scipy.ndimage import gaussian_filter1d
        signal = gaussian_filter1d(signal, sigma=1.5)
        
        axes[idx].fill_between(x, signal, color=colors_map[nuc], alpha=0.7)
        axes[idx].plot(x, signal, color=colors_map[nuc], linewidth=1.5)
        axes[idx].set_ylabel(nuc, fontsize=12, fontweight='bold', rotation=0, labelpad=20)
        axes[idx].set_ylim(-0.3, 1.5)
        axes[idx].grid(alpha=0.2)
        axes[idx].set_yticks([])
    
    axes[-1].set_xlabel('Position (bp)', fontsize=12, fontweight='bold')
    fig.suptitle('DNA Sequencing Signal Chromatogram', fontsize=14, fontweight='bold')
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    visualizations['chromatogram'] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return visualizations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze DNA sequence from text input"""
    try:
        data = request.get_json()
        sequence = data.get('sequence', '').strip()
        
        if not sequence:
            return jsonify({'error': 'No sequence provided'}), 400
        
        # Clean sequence (remove whitespace, numbers, etc.)
        sequence = ''.join(c for c in sequence.upper() if c in 'ATGCN')
        
        if len(sequence) == 0:
            return jsonify({'error': 'Invalid sequence format'}), 400
        
        # Analyze sequence
        analysis = analyze_sequence(sequence)
        
        if 'error' in analysis:
            return jsonify({'error': analysis['error']}), 400
        
        # Generate visualizations
        visualizations = generate_sequence_visualization(sequence, analysis)
        
        return jsonify({
            'success': True,
            'sequence': sequence[:1000],  # Return first 1000 chars
            'full_length': len(sequence),
            'analysis': analysis,
            'visualizations': visualizations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and analyze DNA sequence file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file temporarily
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse sequence from file
        sequence = ""
        try:
            # Try parsing as FASTA/FASTQ
            with open(filepath, 'r') as f:
                records = list(SeqIO.parse(f, 'fasta'))
                if records:
                    sequence = str(records[0].seq)
                else:
                    # Try as plain text
                    f.seek(0)
                    content = f.read()
                    sequence = ''.join(c for c in content.upper() if c in 'ATGCN')
        except:
            # Fallback: read as plain text
            with open(filepath, 'r') as f:
                content = f.read()
                sequence = ''.join(c for c in content.upper() if c in 'ATGCN')
        
        if not sequence:
            os.remove(filepath)
            return jsonify({'error': 'Could not extract DNA sequence from file'}), 400
        
        # Analyze sequence
        analysis = analyze_sequence(sequence)
        
        if 'error' in analysis:
            os.remove(filepath)
            return jsonify({'error': analysis['error']}), 400
        
        # Generate visualizations
        visualizations = generate_sequence_visualization(sequence, analysis)
        
        # Clean up file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'sequence': sequence[:1000],
            'full_length': len(sequence),
            'analysis': analysis,
            'visualizations': visualizations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Simulated AI prediction endpoint for DNA sequence analysis"""
    try:
        data = request.get_json()
        sequence = data.get('sequence', '').strip()
        
        if not sequence:
            return jsonify({'error': 'No sequence provided'}), 400
        
        # Simulate AI model predictions
        # In a real implementation, this would use a trained model
        predictions = {
            'quality_score': np.random.uniform(0.85, 0.99),
            'confidence': np.random.uniform(0.80, 0.95),
            'predicted_features': [
                {
                    'feature': 'Promoter Region',
                    'probability': np.random.uniform(0.3, 0.8),
                    'position': np.random.randint(0, len(sequence) // 2)
                },
                {
                    'feature': 'Coding Sequence',
                    'probability': np.random.uniform(0.5, 0.9),
                    'position': np.random.randint(len(sequence) // 4, len(sequence) // 2)
                },
                {
                    'feature': 'Terminator',
                    'probability': np.random.uniform(0.4, 0.7),
                    'position': np.random.randint(len(sequence) // 2, len(sequence))
                }
            ],
            'variant_calls': [
                {
                    'position': np.random.randint(0, len(sequence)),
                    'reference': 'A',
                    'alternate': 'G',
                    'quality': np.random.uniform(20, 50),
                    'type': 'SNP'
                }
            ] if len(sequence) > 100 else []
        }
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'model_version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Note: Set debug=False in production for security
    # Use environment variable to control debug mode
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
