from textual_serve.server import Server

from pathlib import Path
import shlex
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
APP_COMMAND = f"{shlex.quote(sys.executable)} {shlex.quote(str(PROJECT_ROOT / "src" / "app.py"))}"

server = Server(
    APP_COMMAND,
    host="localhost",
    port=8000,
    title="IA School Map Pathfinder App",
)

def main() -> None:
    server.serve()

if __name__ == "__main__":
    main()
