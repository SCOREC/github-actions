# This file is used as an example of how to chain sbatch commands to restart a
# globus endpoint in the occasion that an endpoint goes down due to maintance

#!/bin/bash
#SBATCH --job-name=Restart
#SBATCH --account=csc679
#SBATCH --nodes=1
#SBATCH --time=00:03:00
#SBATCH --output=last-globus-restart.log
#SBATCH --open-mode=truncate
#SBATCH --begin=00:00

date
ssh login05 << EOF
    hostname
    TZ=America/New_York date
    cd /ccs/home/castia5/globus-compute
    source env.sh
    cd /lustre/orion/csc679/scratch/castia5/globus-compute
    globus-compute-endpoint restart && globus-compute-endpoint list
EOF

sbatch sbatch-restart-globus.sh
