#!/bin/bash
#SBATCH -J LLSVP
#SBATCH -o LLSVP_%j.txt
#SBATCH -e LLSVP_%j.err
#SBATCH -p skx-normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --export=ALL
#SBATCH --time=00:20:00
#SBATCH -A TG-EAR170019
#SBATCH --mail-user=hrmd@mit.edu
#SBATCH --mail-type=all

export OMP_NUM_THREADS=2
export MV2_ENABLE_AFFINITY=0

source /work/06414/tg857131/NormalModes/SetEnv
cd /scratch/06414/tg857131/NormalModes/output/prem_0439.4_2.00_1_00.10_01.00_1

jid=$(echo $SLURM_JOB_ID)
outfile='LLSVP_'$jid'.txt'
errfile='LLSVP_'$jid'.err'

# These lines throttle the rate of I/O.
module use /work/01255/siliu/stampede2/ooops/modulefiles/
module load ooops
export IO_LIMIT_CONFIG=/work/01255/siliu/stampede2/ooops/1.0/conf/config_low
set_io_param 0 low
set_io_param 1 low
set_io_param 2 low

ibrun /work/06414/tg857131/NormalModes/bin/plmvcg_stampede2.out

cp /work/06414/tg857131/NormalModes/bin/$outfile /scratch/06414/tg857131/NormalModes/output/prem_0439.4_2.00_1_00.10_01.00_1
cp /work/06414/tg857131/NormalModes/bin/$errfile /scratch/06414/tg857131/NormalModes/output/prem_0439.4_2.00_1_00.10_01.00_1
