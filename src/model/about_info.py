import subprocess

def run_cmd(cmd:str) -> str:
    return subprocess.check_output(cmd.split()).decode()

OS = run_cmd("lsb_release -a")
KERNEL = run_cmd("uname -a")