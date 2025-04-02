#!/bin/bash
#SBATCH --job-name=pdp_jacobi
#SBATCH --partition=hype
#SBATCH --nodes=1
#SBATCH --ntasks=80
#SBATCH --time=10:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

source /home/intel/oneapi/vtune/2021.1.1/vtune-vars.sh
SAVE_DIR=$HOME
EXEC_DIR=$SCRATCH
cd $EXEC_DIR
export OMP_PROC_BIND=true
rm -rf pdp_run
git clone --depth 1 https://github.com/kerszamaral/pdp_jacobi.git ./pdp_run
cd pdp_run
make clean 
make
time ./gen_results.sh &> out.txt
touch save.tgz
tar cvzf save.tgz --exclude=save.tgz --exclude=.git . || rm save.tgz
mv save.tgz $SAVE_DIR
