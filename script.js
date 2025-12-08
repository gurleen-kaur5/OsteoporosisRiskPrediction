document.getElementById('gender').addEventListener('change', function() {
    const hormonalSelect = document.getElementById('hormonal');
    const selectedGender = this.value;
    
    // Clear current options
    hormonalSelect.innerHTML = '';
    
    if (selectedGender === '') {
        hormonalSelect.disabled = true;
        hormonalSelect.innerHTML = '<option value="">Select gender first...</option>';
    } else {
        hormonalSelect.disabled = false;
        hormonalSelect.innerHTML = '<option value="">Select...</option>';
        hormonalSelect.innerHTML += '<option value="Normal">Normal</option>';
        
        if (selectedGender === 'Female') {
            hormonalSelect.innerHTML += '<option value="Postmenopausal">Postmenopausal</option>';
        } else if (selectedGender === 'Male') {
            hormonalSelect.innerHTML += '<option value="Postmenopausal">Andropause</option>';
        }
    }
});

// Age validation
document.getElementById('age').addEventListener('input', function() {
    const age = parseInt(this.value);
    const errorMsg = document.getElementById('ageError');
    
    if (this.value && (age < 18 || age > 100)) {
        if (!errorMsg) {
            const error = document.createElement('small');
            error.id = 'ageError';
            error.style.color = '#e74c3c';
            error.style.fontSize = '0.85em';
            error.style.marginTop = '5px';
            error.textContent = 'Age must be between 18 and 100 years';
            this.parentElement.appendChild(error);
        }
        this.style.borderColor = '#e74c3c';
    } else {
        if (errorMsg) {
            errorMsg.remove();
        }
        this.style.borderColor = '#e0e0e0';
    }
});

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validate age before submission
    const age = parseInt(document.getElementById('age').value);
    if (age < 18 || age > 100) {
        document.getElementById('errorMessage').textContent = 
            'Please enter a valid age between 18 and 100 years.';
        document.getElementById('errorMessage').style.display = 'block';
        return;
    }
    
    const form = e.target;
    const formData = new FormData(form);
    const data = {};
    
    // Convert form data to object
    for (let [key, value] of formData.entries()) {
        // Handle empty optional fields
        if (value === '') {
            data[key] = null;
        } else if (key === 'Age') {
            data[key] = parseInt(value);
        } else {
            data[key] = value;
        }
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    
    try {
        // REPLACE THIS URL WITH YOUR FLASK API ENDPOINT
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Prediction failed');
        }
        
        const result = await response.json();
        
        // Display results
        displayResult(result);
        
    } catch (error) {
        document.getElementById('errorMessage').textContent = 
            'Error: Unable to connect to prediction server. Please ensure your Flask backend is running on http://localhost:5000';
        document.getElementById('errorMessage').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
    }
});

function displayResult(result) {
    const container = document.getElementById('resultContainer');
    const title = document.getElementById('resultTitle');
    const description = document.getElementById('resultDescription');
    const fill = document.getElementById('confidenceFill');
    
    const isHighRisk = result.prediction === "Osteoporosis Risk Detected";
    const confidence = (result.confidence * 100).toFixed(1);
    
    container.className = 'result-container ' + (isHighRisk ? 'result-high-risk' : 'result-low-risk');
    container.style.display = 'block';
    
    title.textContent = result.prediction;
    
    if (isHighRisk) {
        description.textContent = 'Based on the provided information, there is an elevated risk of osteoporosis. Please consult with a healthcare professional for proper evaluation and guidance.';
    } else {
        description.textContent = 'Based on the provided information, the risk of osteoporosis appears to be low. Continue maintaining healthy lifestyle habits.';
    }
    
    fill.style.width = confidence + '%';
    fill.textContent = confidence + '% Confidence';
}