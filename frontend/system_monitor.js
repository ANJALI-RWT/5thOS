async function fetchStats() {
  const statsRes = await fetch('/api/system_stats');  // relative path
  const stats = await statsRes.json();

  document.getElementById('cpu').textContent = stats.cpu_percent;
  document.getElementById('memory').textContent = stats.memory_percent;
  document.getElementById('disk').textContent = stats.disk_percent;

  const processList = document.getElementById('processes');
  processList.innerHTML = '';
  stats.top_processes.forEach(proc => {
    const li = document.createElement('li');
    li.textContent = `${proc.name} (PID: ${proc.pid}) - CPU: ${proc.cpu_percent}%`;
    processList.appendChild(li);
  });

  const suggestRes = await fetch('/api/optimization_suggestions');  // relative path
  const suggestions = await suggestRes.json();
  const suggestionList = document.getElementById('suggestions');
  suggestionList.innerHTML = '';
  suggestions.suggestions.forEach(s => {
    const li = document.createElement('li');
    li.textContent = s;
    suggestionList.appendChild(li);
  });
}

setInterval(fetchStats, 5000);
fetchStats();
