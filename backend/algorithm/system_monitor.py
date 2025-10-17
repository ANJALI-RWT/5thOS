# backend/algorithms/system_monitor.py
import psutil

def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    # Get top 5 CPU-consuming processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "disk_percent": disk_percent,
        "top_processes": top_processes
    }

def suggest_optimization():
    stats = get_system_stats()
    suggestions = []
    if stats['cpu_percent'] > 80:
        suggestions.append("CPU usage is high. Consider closing heavy apps.")
    if stats['memory_percent'] > 80:
        suggestions.append("Memory usage is high. Consider freeing RAM.")
    if stats['disk_percent'] > 90:
        suggestions.append("Disk usage is critical. Clean up space.")
    return suggestions
