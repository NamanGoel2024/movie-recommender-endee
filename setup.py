import subprocess
import sys
import time
import urllib.request
import os

# Use venv python if it exists, otherwise use current python
VENV_PYTHON = os.path.join(os.path.dirname(__file__), "venv", "bin", "python3")
PYTHON = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

def run_command(command):
    result = subprocess.run(command, shell=True)
    return result.returncode

def check_docker():
    print("Checking Docker...")
    code = run_command("docker --version")
    if code != 0:
        print("Docker not found! Please install Docker first.")
        print("Download from: https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    print("Docker found! ✅")

def start_endee():
    print("\nStarting Endee database...")
    result = subprocess.run(
        "docker ps --filter name=endee-server --format '{{.Names}}'",
        shell=True, capture_output=True, text=True
    )
    if "endee-server" in result.stdout:
        print("Endee already running! ✅")
        return
    code = run_command(
        "docker run -d -p 8080:8080 --name endee-server endeeio/endee-server:latest"
    )
    if code != 0:
        run_command("docker start endee-server")
    print("Waiting for Endee to start", end="")
    for i in range(30):
        try:
            urllib.request.urlopen("http://localhost:8080/api/v1/index/list")
            print("\nEndee is ready! ✅")
            return
        except:
            print(".", end="", flush=True)
            time.sleep(1)
    print("\nEndee took too long to start!")
    sys.exit(1)

def setup_venv():
    print("\nSetting up virtual environment...")
    if not os.path.exists("venv"):
        print("Creating venv...")
        run_command(f"{sys.executable} -m venv venv")
        print("Venv created! ✅")
    else:
        print("Venv already exists! ✅")
    print("Installing dependencies...")
    run_command(f"{VENV_PYTHON} -m pip install -r requirements.txt --quiet")
    print("Dependencies installed! ✅")

def check_index():
    print("\nChecking if movies are loaded in Endee...")
    try:
        response = urllib.request.urlopen("http://localhost:8080/api/v1/index/list")
        data = response.read().decode()
        if "movies" in data:
            print("Movies already loaded! ✅")
        else:
            print("Loading movies into Endee...")
            run_command(f"{VENV_PYTHON} ingest.py")
            print("Movies loaded! ✅")
    except Exception as e:
        print(f"Error checking index: {e}")
        sys.exit(1)

def run_recommender():
    print("\n" + "=" * 60)
    print("Everything is ready! Starting recommender...")
    print("=" * 60 + "\n")
    run_command(f"{VENV_PYTHON} recommend.py")

# Main
if __name__ == "__main__":
    print("🎬 Movie Recommender Setup")
    print("=" * 60)
    check_docker()
    start_endee()
    setup_venv()
    check_index()
    run_recommender()
