const questionsText = [
  "Chest pain / pressure",
  "Shortness of breath",
  "Dizziness / lightheadedness",
  "Palpitations",
  "Extreme fatigue",
  "Swelling in legs",
  "Fainting or near fainting",
  "Leg pain when walking",
  "Family history of heart disease",
  "Smoking severity"
];

// Create questions sliders
function makeQuestion(i, text) {
  const div = document.createElement('div');
  div.className = 'question';
  div.innerHTML = `
    <div><strong>Q${i+1}.</strong> ${text}</div>
    <div class="rangeRow">
      <input type="range" id="q${i+1}" min="1" max="10" value="5" />
      <span id="v${i+1}">5</span>
    </div>
  `;
  const slider = div.querySelector('input');
  const span = div.querySelector('span');
  slider.addEventListener('input', () => span.textContent = slider.value);
  return div;
}

// Append questions
const container = document.getElementById('questions');
questionsText.forEach((text, i) => container.appendChild(makeQuestion(i, text)));

// Handle form submission
document.getElementById('questionForm').addEventListener('submit', async e => {
  e.preventDefault();

  const name = document.getElementById('name').value.trim() || "Anonymous";
  const age = +document.getElementById('age').value;
  const sex = +document.getElementById('sex').value;

  // Collect answers
  const answers = {};
  for (let i = 0; i < questionsText.length; i++) {
    const qId = `q${i+1}`;
    answers[questionsText[i]] = +document.getElementById(qId).value; // use full question text as key
  }

  // Send to backend (keys are now question text)
  const res = await fetch('/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name, age, sex, ...answers})
  });

  const data = await res.json();
  if (!res.ok) return alert('Error: '+data.error);

  // Display answers with full questions, matching UI order
  let summaryText = `Patient Name: ${name}\nAge: ${age}\nSex: ${sex === 1 ? 'Male':'Female'}\n\n`;
  summaryText += `Risk Level: ${data.risk_level}\nRisk Probability: ${data.risk_probability}\nRecommended Tests: ${data.recommended_tests.join(', ')}\n\n`;
  summaryText += "Patient Answers:\n";
  for (let i = 0; i < questionsText.length; i++) {
    const q = questionsText[i];
    if (data.answers && q in data.answers) {
      summaryText += `- ${q}: ${data.answers[q]}\n`;
    }
  }
  document.getElementById('summary').textContent = summaryText;
  document.getElementById('result').classList.remove('hidden');
});
