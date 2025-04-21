#!/bin/bash
#SBATCH --job-name=pdp_jacobi
#SBATCH --partition=hype
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=10:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

source /home/intel/oneapi/vtune/2021.1.1/vtune-vars.sh
SAVE_DIR=$HOME
EXEC_DIR=$SCRATCH
cd $EXEC_DIR
export OMP_PROC_BIND=close
rm -rf ./pdp_run
git clone --depth 1 https://github.com/kerszamaral/pdp_jacobi.git ./pdp_run
cd ./pdp_run
make clean 
make
export VTUNE_ACTIVE=1
time ./get_results.sh 2>&1 >$SAVE_DIR/vtune_pdp_jacobi_slurm.log | tee  -a $SAVE_DIR/vtune_pdp_jacobi_slurm.log > ./vtune_pdp_jacobi_slurm.log
export VTUNE_ACTIVE=""
time ./get_results.sh 2>&1 >$SAVE_DIR/pdp_jacobi_slurm.log | tee  -a $SAVE_DIR/pdp_jacobi_slurm.log > ./pdp_jacobi_slurm.log
touch save.tgz
tar cvzf save.tgz --exclude=save.tgz --exclude=.git . || rm save.tgz
mv save.tgz $SAVE_DIR
