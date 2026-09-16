document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const resetBtn = document.getElementById('reset-btn');
    const symptomInput = document.getElementById('symptom-input');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    
    const inputSection = document.querySelector('.input-section');
    const resultsSection = document.getElementById('results-section');
    
    const predictedDisease = document.getElementById('predicted-disease');
    const analysisText = document.getElementById('analysis-text');
    const remediesList = document.getElementById('remedies-list');
    const doctorsList = document.getElementById('doctors-list');

    analyzeBtn.addEventListener('click', async () => {
        const symptoms = symptomInput.value.trim();
        
        if (!symptoms) {
            alert("Please describe your symptoms first.");
            return;
        }

        // UI Loading State
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symptoms })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Something went wrong.");
            }

            // Populate Data
            predictedDisease.textContent = data.predicted_disease;
            analysisText.textContent = data.analysis;
            
            remediesList.innerHTML = '';
            data.home_remedies.forEach(remedy => {
                const li = document.createElement('li');
                li.textContent = remedy;
                remediesList.appendChild(li);
            });

            doctorsList.innerHTML = '';
            data.recommended_doctors.forEach(doc => {
                const li = document.createElement('li');
                li.textContent = doc;
                doctorsList.appendChild(li);
            });

            // Transition UI
            inputSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');

        } catch (error) {
            alert("Error: " + error.message);
        } finally {
            // Reset Loading State
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        symptomInput.value = '';
        resultsSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
    });
});
