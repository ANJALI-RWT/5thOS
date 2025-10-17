// async function runMemory(){
//   const pages = parsePages(document.getElementById('pages').value);
//   const frames = parseInt(document.getElementById('frames').value || 3);
//   const algo = document.getElementById('memalgo').value;
//   if(pages.length===0){ alert('Enter pages'); return; }

//   // Use backend port 5000
//   const url = algo === 'FIFO'
//     ? 'http://127.0.0.1:5000/api/memory/fifo'
//     : 'http://127.0.0.1:5000/api/memory/lru';

//   const res = await fetch(url, {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({pages: pages, frames: frames})
//   });

//   const data = await res.json();

//   document.getElementById('mem-result').style.display = 'block';
//   const out = document.getElementById('mem-output');
//   out.innerHTML = `<p>Page Faults: <strong>${data.page_faults}</strong></p>`;
  
//   // Show frames over time
//   const rows = data.frames_over_time
//     .map((f, i) => `<div class="small">Step ${i+1}: [${f.join(', ')}]</div>`)
//     .join('');
//   out.innerHTML += rows;
// }
// frontend/memory.js

// Parse a comma-separated string into an array of integers
function parsePages(str) {
  if (!str.trim()) return [];
  return str.split(',').map(x => parseInt(x.trim()));
}

// Run memory management algorithm
async function runMemory() {
  const pages = parsePages(document.getElementById('pages').value);
  const frames = parseInt(document.getElementById('frames').value || 3);
  const algo = document.getElementById('memalgo').value;
  if (pages.length === 0) { alert('Enter pages'); return; }

  const url = algo === 'FIFO'
    ? 'http://127.0.0.1:5000/api/memory/fifo'
    : 'http://127.0.0.1:5000/api/memory/lru';

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pages: pages, frames: frames })
  });

  const data = await res.json();

  document.getElementById('mem-result').style.display = 'block';
  const out = document.getElementById('mem-output');
  out.innerHTML = `<p>Page Faults: <strong>${data.page_faults}</strong></p>`;

  // Show frames over time
  const rows = data.frames_over_time
    .map((f, i) => `<div class="small">Step ${i+1}: [${f.join(', ')}]</div>`)
    .join('');
  out.innerHTML += rows;
}
