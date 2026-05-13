const dropArea = document.getElementById('drop-area');
const fileElem = document.getElementById('fileElem');
const preview = document.getElementById('preview');
const previewImg = document.getElementById('preview-img');
const predictBtn = document.getElementById('predictBtn');
const loader = document.getElementById('loader');
const resultEl = document.getElementById('result');
const resultContent = document.getElementById('resultContent');

let currentFile = null;

// Helpers
function showPreview(file){
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  preview.classList.remove('hidden');
  predictBtn.disabled = false;
  currentFile = file;
}

function hideLoader(){
  loader.classList.add('hidden');
}
function showLoader(){
  loader.classList.remove('hidden');
}

// Drag & drop
['dragenter','dragover','dragleave','drop'].forEach(eventName=>{
  dropArea.addEventListener(eventName,e=>e.preventDefault());
});

dropArea.addEventListener('drop',e=>{
  const dt = e.dataTransfer;
  if(!dt) return;
  const file = dt.files[0];
  if(file) handleFile(file);
});

// Click to open file
dropArea.addEventListener('click',()=> fileElem.click());
fileElem.addEventListener('change',e=>{
  const f = e.target.files[0];
  if(f) handleFile(f);
});

function handleFile(file){
  if(!file.type.startsWith('image/')) return alert('Please upload an image file');
  showPreview(file);
}

// Fake scanning animation (width pulse) — used during upload
function fakeScanEffect(duration=2500){
  const el = document.createElement('div');
  el.style.position='absolute';
  el.style.inset='0';
  el.style.pointerEvents='none';
  el.style.background='linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%)';
  el.style.animation = `scan ${duration}ms linear`;
  el.style.borderRadius='10px';
  el.style.mixBlendMode='overlay';
  el.style.opacity='0.9';
  el.style.zIndex='10';

  preview.appendChild(el);
  setTimeout(()=>{ preview.removeChild(el); }, duration+50);
}

// CSS animation injection for scan
const styleSheet = document.createElement('style');
styleSheet.innerHTML = `@keyframes scan{0%{transform:translateX(-120%)}50%{transform:translateX(0)}100%{transform:translateX(120%)}}`;
document.head.appendChild(styleSheet);

// Predict button
predictBtn.addEventListener('click',async ()=>{
  if(!currentFile) return;
  showLoader();
  resultEl.classList.add('hidden');
  fakeScanEffect(2200);

  try{
    const form = new FormData();
    form.append('file', currentFile);

    const resp = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST', body: form
    });

    if(!resp.ok) throw new Error('Network response not ok');
    const data = await resp.json();

    // show result
    resultContent.innerHTML = `
      <div class="result-pill">${data.material}</div>
      <div class="result-details">
        <div class="label">Confidence</div>
        <div class="value">${data.confidence}</div>
      </div>
    `;
    resultEl.classList.remove('hidden');
  }catch(err){
    alert('Prediction failed: '+err.message);
  }finally{
    hideLoader();
  }
});

// Click on result to clear
resultEl.addEventListener('click',()=>{
  resultEl.classList.add('hidden');
});
