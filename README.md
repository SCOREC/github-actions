# How to test globus compute locally

1. Follow quick start to install globus: 
    - https://globus-compute.readthedocs.io/en/latest/quickstart.html

2. Create an app to use for authentication on:
    - https://www.globus.org/compute
    - this app will be reused for each endpoint you create

3. Generate a secret to use for app created in step 2. I recommend creating a different secret for each endpoint you create.
    - this can not be regenerated so make sure to save it in a secure location and do not share it with anyone else

4. Create the following env file: 
    - replace the app id and secret with the values from step 2 and 3
    - replace the python path with the corresponding path on your account

    module load miniforge3/23.11.0
    source activate localpython
    export GLOBUS_COMPUTE_CLIENT_ID="app id"
    export GLOBUS_COMPUTE_CLIENT_SECRET="secret"
    export PYTHONPATH=$PYTHONPATH:/ccs/home/castia5/.local/frontier/miniforge3/23.11.0/lib/python3.10/site-packages

5. Create an endpoint using
    $globus-compute-endpoint configure
    $globus-compute-endpoint start --detach

6. Run an sbatch script to restart the endpoint periodically for example:
    - https://github.com/SCOREC/github-actions/blob/main/sbatch-restart-globus.sh
    - In this sample script the account number will need to be updated to match your account

7. Copy the following files and run test-globus.sh to test the endpoint
    - https://github.com/SCOREC/github-actions/blob/main/test-globus.sh
    - https://github.com/SCOREC/github-actions/blob/main/run-globus.py

# How change endpoint used by globus compute

1. Copy the id and secret used in previous step 4 into the github secrets for the repository in the following format:
    GLOBUS_CLIENT_ID: app id
    GLOBUS_CLIENT_SECRET: secret

    - Note: the secret should be different for each repo

2. Copy the endpoint id into github action used to run the test here: 
    - https://github.com/SCOREC/github-actions/blob/main/.github/workflows/globus-test.yml
    - Node: this can be public because it requires authentication to use

3. Update path where github test runs in the following locations
    - https://github.com/SCOREC/core/blob/master/.github/workflows/frontier/run.sh
    - https://github.com/SCOREC/core/blob/master/.github/workflows/frontier/install.sh