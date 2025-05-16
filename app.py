from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq
from collections import defaultdict

app = Flask(__name__)
CORS(app)

graph = defaultdict(list)
with open("city_map.txt", "r") as f:
    for line in f:
        a, b, w = line.strip().split()
        graph[a].append((b, int(w)))
        graph[b].append((a, int(w)))

@app.route("/locations")
def get_locations():
    return jsonify(sorted(graph.keys()))

@app.route("/route", methods=["POST"])
def find_route():
    data = request.json
    src = data["start"]
    dest = data["end"]
    visited = set()
    queue = [(0, src, [])]

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == dest:
            return jsonify({"path": path, "cost": cost})
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return jsonify({"path": [], "cost": -1})

if __name__ == "__main__":
    app.run(debug=True)
