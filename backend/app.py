# # backend/app.py
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from algorithms.process_scheduling import fcfs, sjf_nonpreemptive, round_robin
# from algorithms.deadlock import bankers_algorithm
# from algorithms.memory_management import fifo_page_replacement, lru_page_replacement
# from algorithms.disk_scheduling import fcfs_disk, sstf_disk, scan_disk
# import os  # ✅ Added as instructed

# app = Flask(__name__, static_folder="../frontend", static_url_path="/")  # ✅ Added as instructed
# CORS(app)

# # Serve frontend
# @app.route('/<path:path>')
# def serve_page(path):
#     return send_from_directory(app.static_folder, path)

# # Scheduling endpoint
# @app.route('/api/schedule', methods=['POST'])
# def schedule():
#     data = request.json
#     algo = data.get('algorithm', 'FCFS')
#     processes = data.get('processes', [])
    
#     if algo == 'FCFS':
#         result = fcfs(processes)
#     elif algo == 'SJF':
#         result = sjf_nonpreemptive(processes)
#     elif algo == 'RR':
#         quantum = int(data.get('quantum', 2))
#         result = round_robin(processes, quantum)
#     else:
#         return jsonify({"error": "Unknown algorithm"}), 400
    
#     return jsonify(result)

# # Deadlock endpoint
# @app.route('/api/deadlock', methods=['POST'])
# def deadlock():
#     data = request.json
#     allocation = data.get('allocation', [])
#     max_need = data.get('max_need', [])
#     available = data.get('available', [])
    
#     result = bankers_algorithm(allocation, max_need, available)
#     return jsonify(result)

# # Memory endpoints
# @app.route('/api/memory/fifo', methods=['POST'])
# def memory_fifo():
#     data = request.json
#     pages = data.get('pages', [])
#     frames = int(data.get('frames', 3))
#     result = fifo_page_replacement(pages, frames)
#     return jsonify(result)

# @app.route('/api/memory/lru', methods=['POST'])
# def memory_lru():
#     data = request.json
#     pages = data.get('pages', [])
#     frames = int(data.get('frames', 3))
#     result = lru_page_replacement(pages, frames)
#     return jsonify(result)
# from algorithms.system_monitor import get_system_stats, suggest_optimization

# @app.route('/api/system_stats', methods=['GET'])
# def api_system_stats():
#     stats = get_system_stats()
#     return stats  # Flask automatically converts dict to JSON

# @app.route('/api/optimization_suggestions', methods=['GET'])
# def api_optimization_suggestions():
#     suggestions = suggest_optimization()
#     return {"suggestions": suggestions}


# # Disk scheduling
# @app.route('/api/disk', methods=['POST'])
# def disk():
#     data = request.json
#     algo = data.get('algorithm', 'FCFS')
#     requests = data.get('requests', [])
#     head = int(data.get('head', 0))
    
#     if algo == 'FCFS':
#         result = fcfs_disk(requests, head)
#     elif algo == 'SSTF':
#         result = sstf_disk(requests, head)
#     elif algo == 'SCAN':
#         direction = data.get('direction', 'up')
#         result = scan_disk(requests, head, direction)
#     else:
#         result = {"error": "Unknown disk algorithm"}
    
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)







# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from algorithms.process_scheduling import fcfs, sjf_nonpreemptive, round_robin
from algorithms.deadlock import bankers_algorithm
from algorithms.memory_management import fifo_page_replacement, lru_page_replacement
from algorithms.disk_scheduling import fcfs_disk, sstf_disk, scan_disk
from algorithms.system_monitor import get_system_stats, suggest_optimization
import os

frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend')
app = Flask(__name__, static_folder=frontend_path, static_url_path="/")

CORS(app)

# # index.html
# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

# # system_monitor.html
# @app.route('/system_monitor')
# def serve_system_monitor():
#     return send_from_directory(app.static_folder, 'system_monitor.html')

# # fallback: serve any other frontend file
# @app.route('/<path:path>')
# def serve_page(path):
#     return send_from_directory(app.static_folder, path)

# ✅ Serve main index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# ✅ Serve system monitor page
@app.route('/system_monitor')
def serve_system_monitor():
    return send_from_directory(app.static_folder, 'system_monitor.html')

# ✅ Serve other frontend pages (if needed)
@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory(app.static_folder, path)

# Scheduling endpoint
@app.route('/api/schedule', methods=['POST'])
def schedule():
    data = request.json
    algo = data.get('algorithm', 'FCFS')
    processes = data.get('processes', [])
    
    if algo == 'FCFS':
        result = fcfs(processes)
    elif algo == 'SJF':
        result = sjf_nonpreemptive(processes)
    elif algo == 'RR':
        quantum = int(data.get('quantum', 2))
        result = round_robin(processes, quantum)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400
    
    return jsonify(result)

# Deadlock endpoint
@app.route('/api/deadlock', methods=['POST'])
def deadlock():
    data = request.json
    allocation = data.get('allocation', [])
    max_need = data.get('max_need', [])
    available = data.get('available', [])
    
    result = bankers_algorithm(allocation, max_need, available)
    return jsonify(result)

# Memory endpoints
@app.route('/api/memory/fifo', methods=['POST'])
def memory_fifo():
    data = request.json
    pages = data.get('pages', [])
    frames = int(data.get('frames', 3))
    result = fifo_page_replacement(pages, frames)
    return jsonify(result)

@app.route('/api/memory/lru', methods=['POST'])
def memory_lru():
    data = request.json
    pages = data.get('pages', [])
    frames = int(data.get('frames', 3))
    result = lru_page_replacement(pages, frames)
    return jsonify(result)

# ✅ System Monitor API
@app.route('/api/system_stats', methods=['GET'])
def api_system_stats():
    stats = get_system_stats()
    return stats

@app.route('/api/optimization_suggestions', methods=['GET'])
def api_optimization_suggestions():
    suggestions = suggest_optimization()
    return {"suggestions": suggestions}

# Disk scheduling
@app.route('/api/disk', methods=['POST'])
def disk():
    data = request.json
    algo = data.get('algorithm', 'FCFS')
    requests = data.get('requests', [])
    head = int(data.get('head', 0))
    
    if algo == 'FCFS':
        result = fcfs_disk(requests, head)
    elif algo == 'SSTF':
        result = sstf_disk(requests, head)
    elif algo == 'SCAN':
        direction = data.get('direction', 'up')
        result = scan_disk(requests, head, direction)
    else:
        result = {"error": "Unknown disk algorithm"}
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


