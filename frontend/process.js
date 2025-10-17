// frontend/process.js
let processes = [];

function addProcess(){
  const name = document.getElementById('pname').value || `P${processes.length+1}`;
  const burst = parseInt(document.getElementById('burst').value || 0);
  const arrival = parseInt(document.getElementById('arrival').value || 0);
  if(!name || burst<=0){ alert('Enter valid name and burst'); return; }
  processes.push({name:name, burst:burst, arrival:arrival});
  document.getElementById('pname').value=''; 
  document.getElementById('burst').value='';
  renderList();
}

function renderList(){
  const el = document.getElementById('proc-list');
  if(processes.length===0){ 
    el.innerHTML = '<p class="small">No processes added.</p>'; 
    return; 
  }
  let html = '<div class="small"><strong>Processes:</strong> ';
  html += processes.map(p=>`${p.name}(arr:${p.arrival},burst:${p.burst})`).join(' | ');
  html += '</div>';
  el.innerHTML = html;
}

async function run(){
  if(processes.length===0){ alert('Add at least one process'); return; }
  const algo = document.getElementById('algo').value;
  const quantum = parseInt(document.getElementById('quantum').value || 2);
  const payload = {algorithm: algo, processes: processes, quantum: quantum};

  try {
    // ✅ Update fetch to point to Flask backend
    const res = await fetch('http://127.0.0.1:5000/api/schedule', {
      method:'POST', 
      headers:{'Content-Type':'application/json'}, 
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      alert(`Server error: ${res.status} ${res.statusText}`);
      return;
    }

    const data = await res.json();
    showResult(data);

  } catch (err) {
    alert('Error connecting to backend. Make sure Flask is running on port 5000.');
    console.error(err);
  }
}

function showResult(data){
  document.getElementById('result-panel').style.display = 'block';
  const ganttEl = document.getElementById('gantt');
  ganttEl.innerHTML = '';

  const gantt = data.gantt || [];
  if(gantt.length===0){ 
    ganttEl.innerHTML = '<p class="small">No Gantt data</p>'; 
    return; 
  }

  const minStart = Math.min(...gantt.map(g=>g.start));
  const maxEnd = Math.max(...gantt.map(g=>g.end));
  const total = maxEnd - minStart || 1;

  gantt.forEach(segment=>{
    const width = Math.max(6, ((segment.end - segment.start)/total)*100);
    const bar = document.createElement('div'); 
    bar.className='bar';
    bar.style.width = width + '%';
    bar.style.flex = `${segment.end-segment.start} 0 auto`;
    bar.title = `${segment.name}: ${segment.start} -> ${segment.end}`;
    bar.innerText = segment.name;
    ganttEl.appendChild(bar);
  });

  // table
  const tbody = document.querySelector('#details-table tbody'); 
  tbody.innerHTML = '';
  (data.details || []).forEach(d=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${d.name}</td><td>${d.arrival}</td><td>${d.burst}</td><td>${d.start}</td><td>${d.end}</td><td>${d.waiting}</td><td>${d.turnaround}</td>`;
    tbody.appendChild(tr);
  });

  document.getElementById('averages').innerText = `Average Waiting: ${data.avg_wait ?? 'N/A'} , Average Turnaround: ${data.avg_turnaround ?? 'N/A'}`;
}

function clearAll(){
  processes = []; 
  renderList();
  document.getElementById('result-panel').style.display = 'none';
}

window.onload = renderList;
