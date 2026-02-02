// Global variables to store analysis results
let currentResults = null;
let selectedFile = null;

// Example sequences
const examples = {
    short: `>Short Example Sequence
ATGCGATACGCTTACGATCGTAGCTAGCTAGCTAGCTAGCTAGC`,
    
    medium: `>Medium Example Sequence
ATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGACAGTGCGGGCTTTTTTTTTCGACCAAAGGTAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCACCTGGTGGCGATGATTGAAAAAACCATTAGCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATTTTTGCCGAACTTTTGACGGGACTCGCCGCCGCCCAGCCGGGGTTCCCGCTGGCGCAATTGAAAACTTTCGTCGATCAGGAATTTGCCCAAATAAAACATGTCCTGCATGGCATTAGTTTGTTGGGGCAGTGCCCGGATAGCATCAACGCTGCGCTGATTTGCCGTGGCGAGAAAATGTCGATCGCCATTATGGCCGGCGTATTAGAAGCGCGCGGTCACAACGTTACCGTTATCGATCCGGTCGAAAAACTGCTGGCAGTGGGGCATTACCTCGAATCTACCGTCGATATTGCTGAGTCCACCCGCCGTATTGCGGCAAGCCGCATTCCGGCTGATCACATGGTGCTGATGGCAGGTTTCACCGCCGGTAATGAAAAAGGCGAACTGGTGGTGCTTGGACGCAACGGTTCCGACTACTCTGCTGCGGTGCTGGCTGCCTGTTTACGCGCCGATTGTTGCGAGATTTGGACGGACGTTGACGGGGTCTATACCTGCGACCCGCGTCAGGTGCCCGATGCGAGGTTGTTGAAGTCGATGTCCTACCAGGAAGCGATGGAGCTTTCCTACTTCGGCGCTAAAGTTCTTCACCCCCGCACCATTACCCCCATCGCCCAGTTCCAGATCCCTTGCCTGATTAAAAATACCGGAAATCCTCAAGCACCAGGTACGCTCATTGGTGCCAGCCGTGATGAAGACGAATTACCGGTCAAGGGCATTTCCAATCTGAATAACATGGCAATGTTCAGCGTTTCTGGTCCGGGGATGAAAGGGATGGTCGGCATGGCGGCGCGCGTCTTTGCAGCGATGTCACGCGCCCGTATTTCCGTGGTGCTGATTACGCAATCATCTTCCGAATACAGCATCAGTTTCTGCGTTCCACAAAGCGACTGTGTGCGAGCTGAACGGGCAATGCAGGAAGAGTTCTACCTGGAACTGAAAGAAGGCTTACTGGAGCCGCTGGCAGTGACGGAACGGCTGGCCATTATCTCGGTGGTAGGTGATGGTATGCGCACCTTGCGTGGGATCTCGGCGAAATTCTTTGCCGCACTGGCCCGCGCCAATATCAACATTGTCGCCATTGCTCAGGGATCTTCTGAACGCTCAATCTCTGTCGTGGTAAATAACGATGATGCGACCACTGGCGTGCGCGTTACTCATCAGATGCTGTTCAATACCGATCAGGTTATCGAAGTGTTTGTGATTGGCGTCGGTGGCGTTGGCGGTGCGCTGCTGGAGCAACTGAAGCGTCAGCAAAGCTGGCTGAAGAATAAACATATCGACTTACGTGTCTGCGGTGTTGCCAACTCGAAGGCTCTGCTCACCAATGTACATGGCCTTAATCTGGAAAACTGGCAGGAAGAACTGGCGCAAGCCAAAGAGCCGTTTAATCTCGGGCGCTTAATTCGCCTCGTGAAAGAATATCATCTGCTGAACCCGGTCATTGTTGACTGCACCTCCA`,
    
    long: `>Long Example Sequence - Gene with Regulatory Regions
GCTAGCTACGATCGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGACAGTGCGGGCTTTTTTTTTCGACCAAAGGTAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCACCTGGTGGCGATGATTGAAAAAACCATTAGCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATTTTTGCCGAACTTTTGACGGGACTCGCCGCCGCCCAGCCGGGGTTCCCGCTGGCGCAATTGAAAACTTTCGTCGATCAGGAATTTGCCCAAATAAAACATGTCCTGCATGGCATTAGTTTGTTGGGGCAGTGCCCGGATAGCATCAACGCTGCGCTGATTTGCCGTGGCGAGAAAATGTCGATCGCCATTATGGCCGGCGTATTAGAAGCGCGCGGTCACAACGTTACCGTTATCGATCCGGTCGAAAAACTGCTGGCAGTGGGGCATTACCTCGAATCTACCGTCGATATTGCTGAGTCCACCCGCCGTATTGCGGCAAGCCGCATTCCGGCTGATCACATGGTGCTGATGGCAGGTTTCACCGCCGGTAATGAAAAAGGCGAACTGGTGGTGCTTGGACGCAACGGTTCCGACTACTCTGCTGCGGTGCTGGCTGCCTGTTTACGCGCCGATTGTTGCGAGATTTGGACGGACGTTGACGGGGTCTATACCTGCGACCCGCGTCAGGTGCCCGATGCGAGGTTGTTGAAGTCGATGTCCTACCAGGAAGCGATGGAGCTTTCCTACTTCGGCGCTAAAGTTCTTCACCCCCGCACCATTACCCCCATCGCCCAGTTCCAGATCCCTTGCCTGATTAAAAATACCGGAAATCCTCAAGCACCAGGTACGCTCATTGGTGCCAGCCGTGATGAAGACGAATTACCGGTCAAGGGCATTTCCAATCTGAATAACATGGCAATGTTCAGCGTTTCTGGTCCGGGGATGAAAGGGATGGTCGGCATGGCGGCGCGCGTCTTTGCAGCGATGTCACGCGCCCGTATTTCCGTGGTGCTGATTACGCAATCATCTTCCGAATACAGCATCAGTTTCTGCGTTCCACAAAGCGACTGTGTGCGAGCTGAACGGGCAATGCAGGAAGAGTTCTACCTGGAACTGAAAGAAGGCTTACTGGAGCCGCTGGCAGTGACGGAACGGCTGGCCATTATCTCGGTGGTAGGTGATGGTATGCGCACCTTGCGTGGGATCTCGGCGAAATTCTTTGCCGCACTGGCCCGCGCCAATATCAACATTGTCGCCATTGCTCAGGGATCTTCTGAACGCTCAATCTCTGTCGTGGTAAATAACGATGATGCGACCACTGGCGTGCGCGTTACTCATCAGATGCTGTTCAATACCGATCAGGTTATCGAAGTGTTTGTGATTGGCGTCGGTGGCGTTGGCGGTGCGCTGCTGGAGCAACTGAAGCGTCAGCAAAGCTGGCTGAAGAATAAACATATCGACTTACGTGTCTGCGGTGTTGCCAACTCGAAGGCTCTGCTCACCAATGTACATGGCCTTAATCTGGAAAACTGGCAGGAAGAACTGGCGCAAGCCAAAGAGCCGTTTAATCTCGGGCGCTTAATTCGCCTCGTGAAAGAATATCATCTGCTGAACCCGGTCATTGTTGACTGCACCTCCAGCCTGGGTACAATGCTGGCACCGGCAGTGGTCACCATGGGCATGGCCGGCGCGCTGCTGGTGATTTACAACCAGCGCAGGGTGCAGCTGAATCGCGAAGCCGCCATCAACACCAGTGAAGAGAACCTGAACCGGCTGCTGGAAGAGATGCTGCATCGGCTGAAAGAAGAGGCGGCATGGCTGAACATCGAGACCCGCATTCTGAAGAAGGTGAGCAACCATGCGCTGGTGCATGCCGTGGCGACCGTGAAACATCCGGTGACCCATCTGACCGAAGTGGAAAAGAACGTGGTGATTATCGCCGGCGACAGCCAGACCAAGATCATCCTGATCAACGACTACGAGGTGAACAACCGCGTGCTGACCGAACTGCTGAAAGGCCTGACCATTGAGCAGGTGCCGGAAATGACCCTGGTGTACTTCACCGAGAAGTTCAAGGGCGTGAAACAGACCGGCTACACCGGTGGCCAGTACGGTATCGAGACCTGCGTGAAGAACCTGACCTTCAAGGAGCTGCATATCGTGGAGAAGGCAACCAACTAA`
};

// Tab switching
function switchTab(tab) {
    // Update buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.tab-button').classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    if (tab === 'text') {
        document.getElementById('text-tab').classList.add('active');
    } else {
        document.getElementById('file-tab').classList.add('active');
    }
}

// Load example sequences
function loadExample(type) {
    document.getElementById('sequence-input').value = examples[type];
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile = file;
        document.getElementById('selected-file').style.display = 'flex';
        document.getElementById('filename').textContent = file.name;
    }
}

// Clear selected file
function clearFile() {
    selectedFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('selected-file').style.display = 'none';
}

// Show loading indicator
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

// Hide loading indicator
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    hideLoading();
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Analyze sequence from text input
async function analyzeSequence() {
    const sequence = document.getElementById('sequence-input').value.trim();
    
    if (!sequence) {
        showError('Please enter a DNA sequence');
        return;
    }
    
    showLoading();
    
    try {
        // Send sequence for analysis
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sequence: sequence })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        currentResults = data;
        
        // Get AI predictions
        const predictResponse = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sequence: data.sequence })
        });
        
        const predictions = await predictResponse.json();
        currentResults.predictions = predictions.predictions;
        
        displayResults(currentResults);
        hideLoading();
    } catch (error) {
        showError('Error: ' + error.message);
    }
}

// Upload and analyze file
async function uploadAndAnalyze() {
    if (!selectedFile) {
        showError('Please select a file to upload');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        currentResults = data;
        
        // Get AI predictions
        const predictResponse = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sequence: data.sequence })
        });
        
        const predictions = await predictResponse.json();
        currentResults.predictions = predictions.predictions;
        
        displayResults(currentResults);
        hideLoading();
    } catch (error) {
        showError('Error: ' + error.message);
    }
}

// Display results
function displayResults(data) {
    document.getElementById('results').style.display = 'block';
    
    // Display AI predictions
    displayPredictions(data.predictions);
    
    // Display statistics
    displayStatistics(data.analysis);
    
    // Display visualizations
    displayVisualizations(data.visualizations);
    
    // Display detailed analysis
    displayDetailedAnalysis(data);
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

// Display AI predictions
function displayPredictions(predictions) {
    const container = document.getElementById('predictions-content');
    
    let html = `
        <div class="prediction-item">
            <h3>Quality Score</h3>
            <p>${(predictions.quality_score * 100).toFixed(1)}% - High confidence in sequence accuracy</p>
            <div class="prediction-bar">
                <div class="prediction-bar-fill" style="width: ${predictions.quality_score * 100}%"></div>
            </div>
        </div>
        
        <div class="prediction-item">
            <h3>Analysis Confidence</h3>
            <p>${(predictions.confidence * 100).toFixed(1)}% - Model confidence in predictions</p>
            <div class="prediction-bar">
                <div class="prediction-bar-fill" style="width: ${predictions.confidence * 100}%"></div>
            </div>
        </div>
        
        <div class="prediction-item">
            <h3>Predicted Features</h3>
    `;
    
    predictions.predicted_features.forEach(feature => {
        html += `
            <div style="margin-bottom: 0.5rem;">
                <strong>${feature.feature}</strong> at position ${feature.position} 
                (${(feature.probability * 100).toFixed(1)}% confidence)
                <div class="prediction-bar">
                    <div class="prediction-bar-fill" style="width: ${feature.probability * 100}%"></div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    if (predictions.variant_calls && predictions.variant_calls.length > 0) {
        html += `
            <div class="prediction-item">
                <h3>Variant Calls</h3>
                ${predictions.variant_calls.map(v => `
                    <div>Position ${v.position}: ${v.reference} → ${v.alternate} 
                    (Quality: ${v.quality.toFixed(1)}, Type: ${v.type})</div>
                `).join('')}
            </div>
        `;
    }
    
    container.innerHTML = html;
}

// Display statistics
function displayStatistics(analysis) {
    const container = document.getElementById('statistics-content');
    
    const stats = [
        { label: 'Sequence Length', value: `${analysis.length} bp` },
        { label: 'GC Content', value: `${analysis.gc_content}%` },
        { label: 'A Count', value: analysis.a_count },
        { label: 'T Count', value: analysis.t_count },
        { label: 'G Count', value: analysis.g_count },
        { label: 'C Count', value: analysis.c_count },
        { label: 'Molecular Weight', value: `${analysis.molecular_weight} Da` },
        { label: 'ORFs Found', value: analysis.orfs.length }
    ];
    
    container.innerHTML = stats.map(stat => `
        <div class="stat-item">
            <span class="stat-value">${stat.value}</span>
            <span class="stat-label">${stat.label}</span>
        </div>
    `).join('');
}

// Display visualizations
function displayVisualizations(visualizations) {
    if (visualizations.chromatogram) {
        document.getElementById('chromatogram-content').innerHTML = 
            `<img src="data:image/png;base64,${visualizations.chromatogram}" alt="Chromatogram">`;
    }
    
    if (visualizations.composition) {
        document.getElementById('composition-content').innerHTML = 
            `<img src="data:image/png;base64,${visualizations.composition}" alt="Nucleotide Composition">`;
    }
    
    if (visualizations.gc_distribution) {
        document.getElementById('gc-distribution-content').innerHTML = 
            `<img src="data:image/png;base64,${visualizations.gc_distribution}" alt="GC Distribution">`;
    }
    
    if (visualizations.gc_skew) {
        document.getElementById('gc-skew-content').innerHTML = 
            `<img src="data:image/png;base64,${visualizations.gc_skew}" alt="GC Skew">`;
    }
}

// Display detailed analysis
function displayDetailedAnalysis(data) {
    const analysis = data.analysis;
    
    // Sequence details
    const sequenceHtml = `
        <div class="sequence-display">
            <h4>Original Sequence (first 500 bp):</h4>
            <div>${formatSequence(data.sequence.substring(0, 500))}</div>
            ${data.full_length > 500 ? `<p>... (${data.full_length - 500} more bases)</p>` : ''}
            
            <h4 style="margin-top: 1rem;">Complement:</h4>
            <div>${formatSequence(analysis.complement.substring(0, 500))}</div>
            
            <h4 style="margin-top: 1rem;">Reverse Complement:</h4>
            <div>${formatSequence(analysis.reverse_complement.substring(0, 500))}</div>
        </div>
    `;
    document.getElementById('sequence-details').innerHTML = sequenceHtml;
    
    // ORFs
    let orfsHtml = '<p>Open Reading Frames (ORFs) are stretches of DNA that begin with a start codon (ATG) and end with a stop codon.</p>';
    
    if (analysis.orfs.length > 0) {
        orfsHtml += `
            <table class="orf-table">
                <thead>
                    <tr>
                        <th>Start</th>
                        <th>End</th>
                        <th>Length</th>
                        <th>Frame</th>
                        <th>Strand</th>
                        <th>Sequence Preview</th>
                    </tr>
                </thead>
                <tbody>
                    ${analysis.orfs.map(orf => `
                        <tr>
                            <td>${orf.start}</td>
                            <td>${orf.end}</td>
                            <td>${orf.length} bp</td>
                            <td>${orf.frame}</td>
                            <td>${orf.strand}</td>
                            <td><code>${orf.sequence.substring(0, 30)}...</code></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else {
        orfsHtml += '<p>No ORFs found (minimum length: 75 bp)</p>';
    }
    document.getElementById('orfs-content').innerHTML = orfsHtml;
    
    // Translation
    const translationHtml = `
        <div class="sequence-display">
            <h4>RNA Transcription:</h4>
            <div>${formatSequence(analysis.rna.substring(0, 500))}</div>
            
            <h4 style="margin-top: 1rem;">Protein Translation:</h4>
            <div style="word-break: break-all;">${analysis.protein.substring(0, 200)}</div>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;">
                Note: Translation may include stop codons (*) and assumes standard genetic code.
            </p>
        </div>
    `;
    document.getElementById('translation-content').innerHTML = translationHtml;
}

// Format sequence with colors
function formatSequence(sequence) {
    return sequence.split('').map(base => {
        const className = `nuc-${base.toLowerCase()}`;
        return `<span class="${className}">${base}</span>`;
    }).join('');
}

// Switch analysis tabs
function switchAnalysisTab(tab) {
    // Update buttons
    document.querySelectorAll('.analysis-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update content
    document.querySelectorAll('.analysis-tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    if (tab === 'sequence') {
        document.getElementById('sequence-details-tab').classList.add('active');
    } else if (tab === 'orfs') {
        document.getElementById('orfs-tab').classList.add('active');
    } else if (tab === 'translation') {
        document.getElementById('translation-tab').classList.add('active');
    }
}

// Export results
function exportResults(format) {
    if (!currentResults) {
        showError('No results to export');
        return;
    }
    
    let content = '';
    let filename = '';
    let mimeType = '';
    
    if (format === 'json') {
        content = JSON.stringify(currentResults, null, 2);
        filename = 'dna_analysis_results.json';
        mimeType = 'application/json';
    } else if (format === 'txt') {
        content = generateTextReport(currentResults);
        filename = 'dna_analysis_results.txt';
        mimeType = 'text/plain';
    } else if (format === 'csv') {
        content = generateCSVReport(currentResults);
        filename = 'dna_analysis_results.csv';
        mimeType = 'text/csv';
    }
    
    // Create and download file
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Generate text report
function generateTextReport(data) {
    const analysis = data.analysis;
    const predictions = data.predictions;
    
    let report = 'DNA SEQUENCE ANALYSIS REPORT\n';
    report += '=' .repeat(50) + '\n\n';
    
    report += 'BASIC STATISTICS\n';
    report += '-'.repeat(50) + '\n';
    report += `Sequence Length: ${analysis.length} bp\n`;
    report += `GC Content: ${analysis.gc_content}%\n`;
    report += `A: ${analysis.a_count}, T: ${analysis.t_count}, G: ${analysis.g_count}, C: ${analysis.c_count}\n`;
    report += `Molecular Weight: ${analysis.molecular_weight} Da\n\n`;
    
    if (predictions) {
        report += 'AI PREDICTIONS\n';
        report += '-'.repeat(50) + '\n';
        report += `Quality Score: ${(predictions.quality_score * 100).toFixed(1)}%\n`;
        report += `Confidence: ${(predictions.confidence * 100).toFixed(1)}%\n\n`;
    }
    
    report += 'OPEN READING FRAMES\n';
    report += '-'.repeat(50) + '\n';
    if (analysis.orfs.length > 0) {
        analysis.orfs.forEach((orf, i) => {
            report += `ORF ${i + 1}: Position ${orf.start}-${orf.end}, Length ${orf.length} bp, Frame ${orf.frame}\n`;
        });
    } else {
        report += 'No ORFs found\n';
    }
    
    report += '\n' + '='.repeat(50) + '\n';
    report += 'End of Report\n';
    
    return report;
}

// Generate CSV report
function generateCSVReport(data) {
    const analysis = data.analysis;
    
    let csv = 'Metric,Value\n';
    csv += `Sequence Length,${analysis.length}\n`;
    csv += `GC Content,${analysis.gc_content}\n`;
    csv += `A Count,${analysis.a_count}\n`;
    csv += `T Count,${analysis.t_count}\n`;
    csv += `G Count,${analysis.g_count}\n`;
    csv += `C Count,${analysis.c_count}\n`;
    csv += `Molecular Weight,${analysis.molecular_weight}\n`;
    csv += `ORFs Found,${analysis.orfs.length}\n`;
    
    return csv;
}
