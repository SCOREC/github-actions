# This file will connect to an endpoint and run the supplied mashine file on that endpoint

from globus_compute_sdk import Executor
import sys
import os

machine = sys.argv[1]
name = sys.argv[2]
branch = sys.argv[3]
endpoint = sys.argv[4]

with open(machine+'/install.sh', 'r') as file:
    install_file = file.read()

with open(machine+'/run.sh', 'r') as file:
    run_file = file.read()

def get_working_dir():
    import os
    return os.getcwd()

def run_on_endpoint(name, branch, install_file, run_file):
    import subprocess
    import os

    os.makedirs(name+"-test", exist_ok=True)

    with open(name+"-test/install.sh", "w") as text_file:
        text_file.write("%s" % install_file)
        text_file.close()
    
    with open(name+"-test/run.sh", "w") as text_file:
        text_file.write("%s" % run_file)
        text_file.close()

    install_command = "cd {0}-test && chmod +x install.sh && ./install.sh {1} 2>&1 | tee build.log".format(name, branch)
    install_result = subprocess.run([install_command], shell=True, encoding="utf_8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if install_result.returncode != 0:
        return (install_result, None)

    run_command = "cd {0}-test && chmod +x run.sh && ./run.sh 2>&1 | tee test.log".format(name)
    run_result = subprocess.run([run_command], shell=True, encoding="utf_8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return (install_result, run_result)

print ("===Running tests on endpoint, this might take a few minutes===")
gce = Executor(endpoint_id = endpoint)
print ("Running at {0}".format(gce.submit(get_working_dir).result()))

future = gce.submit(run_on_endpoint, name, branch, install_file, run_file)
result = future.result()

with open("Build.log", "w") as text_file:
    text_file.write("%s" % result[0].stdout)
    text_file.close()

if result[1] != None:
    with open("Test.log", "w") as text_file:
        text_file.write("%s" % result[1].stdout)
        text_file.close()

print ("Done: output written to Build.log and Test.log in "+ os.getcwd())
