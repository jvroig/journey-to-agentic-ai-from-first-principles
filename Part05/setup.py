import subprocess
import sys
import os

def create_venv(python_version):
    subprocess.run([python_version, "-m", "venv", "venv"])

def generate_bash_script():
    # Generate bash script to activate venv, install dependencies, and start server
    commands = []

    if os.name == "nt":
        activate_script = "/".join(["venv", "Scripts", "activate"])
        pip_path = "/".join(['venv', 'Scripts', 'pip'])
        python_path = "/".join(['venv', 'Scripts', 'python'])
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        pip_path = os.path.join('venv', 'bin', 'pip')
        python_path = os.path.join('venv', 'bin', 'python')

    commands.append(f"source {activate_script}")
    commands.append(f"{pip_path} install -r requirements.txt")
    commands.append(f"{python_path} qwen_api.py")

    return "\n".join(commands)

def main():
    if len(sys.argv) > 1:
        python_version = sys.argv[1]
    else:
        python_version = sys.executable
    
    create_venv(python_version)
    
    # Generate bash script
    bash_script = generate_bash_script()

    with open('start.sh', 'w') as f:
        f.write(bash_script)

    print("Setup script written successfully! To start, please run: bash start.sh")

if __name__ == "__main__":
    main()
