#This file is used as an example on how to run the run-globus.py file

# Instructions:
# 1. Copy this file and run-globus.py into the same directory
# 2. Follow instructions in run-globus.py
# 3. Edit inputs in this file to desired test
# 4. Execute this file

# inputs
machine=frontier
repo=omega_h
branch=master
endpoint=d625c6cf-de7a-4228-ac44-56247a642fe0

# execution
dir=$PWD

source env.sh
rm $repo -rf
git clone https://github.com/SCOREC/$repo
cd $repo/.github/workflows/
git checkout $branch


python $dir/run-globus.py $machine $repo $branch $endpoint
