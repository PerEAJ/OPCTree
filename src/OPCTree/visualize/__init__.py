import os
import http.server
import socketserver
import socket
import threading
import webbrowser
import json
from pathlib import Path

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def start_server_in_background(directory, port=8000):
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            # Översätt sökvägen till den angivna katalogen
            path = super().translate_path(path)
            relative_path = os.path.relpath(path, os.getcwd())
            return os.path.join(directory, relative_path)

    handler = CustomHTTPRequestHandler

    def serve():
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌍 Server startad på http://localhost:{port}/ (tryck Ctrl+C för att stoppa i terminalen)")
            httpd.serve_forever()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()

def generate_html_visualization(root_node, start_server=True, port=8000):
    def serialize_node(node):
        return {
            "name": ('.' + str(node.opc_path)).split('.')[-1],
            "type": node.__class__.__name__,
            "opc_properties": getattr(node, "name_prop", {}),
            "children": [serialize_node(getattr(node,child)) for child in getattr(node, "opc_children", [])]
        }

    tree_data = serialize_node(root_node)

    json_path = Path(__file__).parent / "vis_tree.json"

    with open(json_path, "w", encoding="utf-8") as json_file:
        tree_json = json.dumps(tree_data, indent=2)
        json_file.write(tree_json)

    print(f"json-fil genererad: {json_path}")

    url = f"http://localhost:{port}/vis_template.html"

    if start_server:
        if is_port_in_use(port):
            print(f"⚠️ Port {port} används redan. Laddar bara sidan.")
        else:
            start_server_in_background(Path(__file__).parent, port)
    else:
        print("📁 Serverstart inaktiverad.")

    webbrowser.open(url, new=2)