#!/bin/bash 

#SBATCH -N 1                      # node count
#SBATCH -n 16                        # number of cores
#SBATCH -t 1-00:00                  # wall time (D-HH:MM)
#SBATCH -p general              # partition
#SBATCH -q public              # QOS 'queue' # ftimmes
#SBATCH -o slurm1.out             # STDOUT (%j = JobId)
#SBATCH -e slurm1.err             # STDERR (%j = JobId)
#SBATCH --mem=32G         # memory (4G is default)
#SBATCH --mail-type=END,FAIL             # notifications for job done & fail
#SBATCH --mail-user=ekfarag@asu.edu # send-to address

module purge

export TMPDIR=$(mktemp -d --tmpdir=/scratch/ekfarag/tmp)
export OMP_NUM_THREADS=16
export ScratchDir="/."
#mkdir -p $ScratchDir
#echo $ScratchDir
module load shpc/python/3.9.2-slim/module
module load git-lfs-3.3.0-gcc-11.2.0
export MESA_DIR=/scratch/ekfarag/MESA_INSTALLATION/mesa-r24.08.1
export MESASDK_ROOT=/scratch/ekfarag/nc_neutrinos/mesasdk
source $MESASDK_ROOT/bin/mesasdk_init.sh
#cd /scratch/ekfarag/OPAL_AGSS09/1
#sleep -50
./clean
./mk
./rn




date

exit 0
