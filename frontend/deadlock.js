// frontend/deadlock.js
function parseMatrix(str){
  // "1,0,0;0,2,1" => [[1,0,0],[0,2,1]]
  if(!str.trim()) return [];
  return str.split(';').map(r => r.split(',').map(x=>parseInt(x.trim())));
}
function parseVector(str){
  if(!str.trim()) return [];
  return str.split(',').map(x=>parseInt(x.trim()));
}
async function runDeadlock(){
  const alloc = parseMatrix(document.getElementById('allocation').value);
  const maxneed = parseMatrix(document.getElementById('maxneed').value);
  const avail = parseVector(document.getElementById('available').value);
  const payload = {allocation: alloc, max_need: maxneed, available: avail};
const res = await fetch('http://127.0.0.1:5000/api/deadlock', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
});
  const data = await res.json();
  document.getElementById('dead-result').style.display = 'block';
  const out = document.getElementById('dead-output');
  if(data.is_safe){
    out.innerHTML = `<p>System is <strong>SAFE</strong>. Safe sequence (process indices): ${data.safe_sequence.join(', ')}</p>`;
  } else {
    out.innerHTML = `<p>System is <strong>UNSAFE</strong>. Deadlock may occur.</p>`;
  }
}
