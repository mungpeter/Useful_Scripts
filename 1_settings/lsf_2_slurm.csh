#!/bin/csh

#
#  Peter M.U. Ung @ gRED
#
#  v1	20.04.25
#
#  convert Torque LSF input file to Slurm input format
#  need to check *Time* and *node*
#

if ($#argv != 2) then
  echo ''
  echo '  > {0}.csh <input LSF script>  <output Slurm script>'
  echo ''
  exit
endif


grep -v ' -B' $argv[1] | \
grep -v ' -N'  | \
grep -v ' -u ' | \
grep -v ' -L ' | \
grep -v 'v100' | \
grep -v 'p100' | \
sed 's/BSUB/SBATCH/g' | \
sed 's/-P .*$/-p defq\t\t# defq; himem; gpu/g' | \
sed 's/-q .*$/--qos=medium\t# veryshort=10m;short=2h;medium=1d;long=3d;verylong=14d/g' | \
sed 's/-R "rusage\[ngpus_excl_p=.*\]"/--gres=gpu:volta:XXX/g' | \
sed 's/-R "span\[ptile=.*\]"/--ntasks-per-node=XXX/g' | \
sed 's/BATCH -W /BATCH -t [d-HH:MM:SS]/g' | \
sed 's/lsf/slu/g' | \
sed 's/bkill -J /scancel -n /g' | \
sed 's/bkill /scancel /g' \
sed 's/bsub </sbatch/g' | \
sed 's/qsub/sbatch/g' | \
sed 's/ungp01/ungm/g' \
  > $argv[2]

