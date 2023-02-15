import subprocess

def execute_gen(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()


def execute(cmd, silent=False):
    for line in execute_gen(cmd):
        if not silent:
            print(line, end='')
