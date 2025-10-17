// frontend/disk.js
function parseReqs(str){
  if(!str.trim()) return [];
  return str.split(',').map(x => parseInt(x.trim()));
}

async function runDisk(){
  const reqs = parseReqs(document.getElementById('requests').value);
  const head = parseInt(document.getElementById('head').value || 0);
  const algo = document.getElementById('diskalgo').value;
  const direction = document.getElementById('dir').value;

  if(reqs.length === 0){
    alert('Enter requests');
    return;
  }

  const payload = {requests: reqs, head: head, algorithm: algo, direction: direction};

  // ✅ Use backend URL explicitly
  const res = await fetch('http://127.0.0.1:5000/api/disk', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  document.getElementById('disk-result').style.display = 'block';
  const out = document.getElementById('disk-output');
  
  if(data.order){
    out.innerHTML = `<p>Order: ${data.order.join(', ')}</p><p>Total Seek: ${data.total_seek}</p>`;
  } else {
    out.innerHTML = `<p>Error: ${data.error || 'Unknown error'}</p>`;
  }
}
