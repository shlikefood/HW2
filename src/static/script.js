const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadContent = document.getElementById('uploadContent');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.querySelector('.btn-text');
const spinner = document.querySelector('.spinner');
const resultBox = document.getElementById('resultBox');
const ageResult = document.getElementById('ageResult');
const genderResult = document.getElementById('genderResult');
const errorBox = document.getElementById('errorBox');
let selectedFile = null;

uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.classList.add('dragover'); });
uploadArea.addEventListener('dragleave', () => { uploadArea.classList.remove('dragover'); });
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault(); uploadArea.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) handleFile(e.target.files[0]);
});

function handleFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) return showError("Please upload a valid image file (JPG, PNG).");
    selectedFile = file; hideError(); resultBox.classList.add('hidden');
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result; imagePreview.classList.remove('hidden');
        uploadContent.classList.add('hidden'); analyzeBtn.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    btnText.classList.add('hidden'); spinner.classList.remove('hidden');
    analyzeBtn.style.pointerEvents = 'none'; resultBox.classList.add('hidden'); hideError();
    const formData = new FormData(); formData.append('file', selectedFile);
    try {
        const response = await fetch('/predict/', { method: 'POST', body: formData });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Something went wrong.");
        setTimeout(() => {
            ageResult.textContent = data.predicted_age; genderResult.textContent = data.predicted_gender;
            ageResult.classList.add('neon'); genderResult.classList.add('neon');
            resultBox.classList.remove('hidden'); resetBtn();
        }, 600);
    } catch (err) { showError(err.message); resetBtn(); }
});

function resetBtn() { btnText.classList.remove('hidden'); spinner.classList.add('hidden'); analyzeBtn.style.pointerEvents = 'auto'; }
function showError(msg) { errorBox.textContent = msg; errorBox.classList.remove('hidden'); }
function hideError() { errorBox.classList.add('hidden'); errorBox.textContent = ''; }
