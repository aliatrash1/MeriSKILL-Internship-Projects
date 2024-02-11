document.addEventListener('DOMContentLoaded', function () {
    // Display any initialization logic here
});

function predict() {
    // Get user input values
    var pregnancies = parseFloat(document.getElementById('pregnancies').value);
    var glucose = parseFloat(document.getElementById('glucose').value);
    var bloodPressure = parseFloat(document.getElementById('blood-pressure').value);
    var skinThickness = parseFloat(document.getElementById('skin-thickness').value);
    var insulin = parseFloat(document.getElementById('insulin').value);
    var bmi = parseFloat(document.getElementById('bmi').value);
    var dpf = parseFloat(document.getElementById('dpf').value);
    var age = parseFloat(document.getElementById('age').value);
    // Repeat the following for other input features (blood pressure, etc.)

    // Sample input data (replace this with the actual input from the user)
    var inputData = {
        'pregnancies': pregnancies,
        'glucose': glucose,
        'blood_pressure': bloodPressure,
        'skin_thickness': skinThickness,
        'insulin': insulin,
        'bmi': bmi,
        'diabetes_pedigree_function': dpf,
        'age': age
      };


    // Make a POST request to the Flask server for prediction
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('predictions').textContent = 'Result: ' + (data.prediction == 1? 'Risk of diabetes' : 'No risk of diabetes');
    })
    .catch(error => {
        console.error('Error:', error);
    });
    console.log('pressed')
}
