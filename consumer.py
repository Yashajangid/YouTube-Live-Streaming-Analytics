import requests
import pandas as pd
from flask import Flask, request, jsonify, render_template_string
from collections import defaultdict
import time
import threading

app = Flask(__name__)
stats = defaultdict(lambda: {'views': 0, 'likes': 0, 'dislikes': 0, 'title': ''})
live_count = 0

def poll_data():
    global live_count
    while True:
        try:
            r = requests.get('http://10.178.7.241:5000/consume')
            data = r.json()
            for msg in data:
                vid = msg['video_id']
                stats[vid]['views'] += msg['views']
                stats[vid]['likes'] += msg['likes']
                stats[vid]['dislikes'] += msg['dislikes']
                stats[vid]['title'] = msg['title'][:60]
            live_count = len(stats)
            print(f"📊 LIVE: {live_count} videos streaming")
        except:
            pass
        time.sleep(1)

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📺 YouTube Live Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        .header { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(20px); 
            border-radius: 20px; 
            padding: 30px; 
            text-align: center; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .header h1 { 
            font-size: 2.5em; 
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            margin-bottom: 10px;
        }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 25px; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-10px); }
        .stat-number { font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
        
        .controls { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(20px); 
            padding: 25px; 
            border-radius: 20px; 
            margin-bottom: 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .control-group { display: flex; gap: 15px; flex-wrap: wrap; align-items: center; }
        input, select, button { 
            padding: 12px 20px; 
            border: none; 
            border-radius: 25px; 
            font-size: 16px; 
            transition: all 0.3s ease;
        }
        input, select { background: #f8f9fa; border: 2px solid #e9ecef; }
        input:focus, select:focus { outline: none; border-color: #4ecdc4; transform: scale(1.02); }
        button { 
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
            color: white; 
            cursor: pointer; 
            font-weight: bold;
        }
        button:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        
        .table-container { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(20px); 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        table { width: 100%; border-collapse: collapse; }
        th { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 20px; 
            text-align: left; 
            font-weight: 600; 
            position: sticky; top: 0;
        }
        td { 
            padding: 18px 20px; 
            border-bottom: 1px solid #eee; 
            transition: background 0.3s ease;
        }
        tr:hover { background: #f8f9fa; transform: scale(1.01); }
        .title { font-weight: 500; max-width: 300px; }
        .views, .likes { font-weight: bold; color: #28a745; }
        .dislikes { color: #dc3545; }
        .engagement { color: #007bff; font-weight: bold; }
        
        .live-indicator { 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            background: #28a745; 
            color: white; 
            padding: 10px 20px; 
            border-radius: 25px; 
            font-weight: bold; 
            box-shadow: 0 5px 15px rgba(40,167,69,0.4);
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(40,167,69,0.7); } 70% { box-shadow: 0 0 0 10px rgba(40,167,69,0); } 100% { box-shadow: 0 0 0 0 rgba(40,167,69,0); } }
        
        @media (max-width: 768px) { .control-group { flex-direction: column; align-items: stretch; } }
    </style>
</head>
<body>
    <div class="live-indicator" id="liveIndicator">
        <i class="fas fa-circle"></i> LIVE <span id="liveCount">0</span> Videos
    </div>
    
    <div class="container">
        <div class="header">
            <h1><i class="fab fa-youtube"></i> YouTube Live Streaming Analytics</h1>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="totalViews">0</div>
                    <div>Total Views</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalLikes">0</div>
                    <div>Total Likes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="videoCount">0</div>
                    <div>Videos</div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <input type="number" id="minViews" placeholder="Minimum Views" value="0">
                <select id="sortBy">
                    <option value="views">Sort by Views</option>
                    <option value="likes">Sort by Likes</option>
                    <option value="engagement">Engagement %</option>
                </select>
                <button onclick="applyFilters()"><i class="fas fa-filter"></i> Filter</button>
                <button onclick="clearFilters()"><i class="fas fa-redo"></i> Reset</button>
            </div>
        </div>
        
        <div class="table-container">
            <table id="videoTable">
                <thead>
                    <tr>
                        <th><i class="fas fa-trophy"></i> Rank</th>
                        <th><i class="fas fa-video"></i> Video Title</th>
                        <th><i class="fas fa-eye"></i> Views</th>
                        <th><i class="fas fa-thumbs-up"></i> Likes</th>
                        <th><i class="fas fa-thumbs-down"></i> Dislikes</th>
                        <th><i class="fas fa-heart"></i> Engagement</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
    </div>

    <script>
        let allData = [];
        
        function updateDashboard() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    allData = data;
                    updateLiveIndicator(data.length);
                    updateStats(data);
                    renderTable(data);
                });
        }
        
        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            const minViews = parseInt(document.getElementById('minViews').value) || 0;
            const sortBy = document.getElementById('sortBy').value;
            
            let filtered = data.filter(row => parseFloat(row.views.replace(/,/g,'')) >= minViews);
            
            filtered.sort((a,b) => {
                let valA = parseFloat(a[sortBy].replace(/,/g,'') || 0);
                let valB = parseFloat(b[sortBy].replace(/,/g,'') || 0);
                return sortBy === 'engagement' ? valB - valA : valB - valA;
            });
            
            tbody.innerHTML = filtered.slice(0, 50).map((row, i) => `
                <tr>
                    <td><strong>#${i+1}</strong></td>
                    <td class="title">${row.title}</td>
                    <td class="views">${row.views}</td>
                    <td class="likes">${row.likes}</td>
                    <td class="dislikes">${row.dislikes}</td>
                    <td class="engagement">${row.engagement}</td>
                </tr>
            `).join('');
        }
        
        function updateStats(data) {
            const totalViews = data.reduce((sum, row) => sum + parseFloat(row.views.replace(/,/g,'')), 0);
            const totalLikes = data.reduce((sum, row) => sum + parseFloat(row.likes.replace(/,/g,'')), 0);
            
            document.getElementById('totalViews').textContent = totalViews.toLocaleString();
            document.getElementById('totalLikes').textContent = totalLikes.toLocaleString();
            document.getElementById('videoCount').textContent = data.length;
        }
        
        function updateLiveIndicator(count) {
            document.getElementById('liveCount').textContent = count;
        }
        
        function applyFilters() { renderTable(allData); }
        function clearFilters() { 
            document.getElementById('minViews').value = 0;
            document.getElementById('sortBy').value = 'views';
            renderTable(allData); 
        }
        
        // Auto-refresh every 2 seconds
        setInterval(updateDashboard, 2000);
        updateDashboard(); // Initial load
    </script>
</body>
</html>
    '''

@app.route('/api/stats')
def api_stats():
    df_list = []
    for vid, data in stats.items():
        df_list.append({
            'video_id': vid,
            'title': data['title'],
            'views': f"{data['views']:,.0f}",
            'likes': f"{data['likes']:,.0f}",
            'dislikes': f"{data['dislikes']:,.0f}",
            'engagement': f"{data['likes']/max(data['views'],1)*100:.1f}%"
        })
    return jsonify(df_list)

if __name__ == '__main__':
    threading.Thread(target=poll_data, daemon=True).start()
    print("🚀 PROFESSIONAL Dashboard: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)