from textual_serve.server import Server
import sys

server = Server(
    f"PYTHONPATH=src {sys.executable} -m app",
    host="127.0.0.1",
    port=8000,
    title="IA School Map Pathfinder App",
)

server.serve()
