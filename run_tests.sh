#!/bin/bash
#SBATCH --account=def-maxwl
#SBATCH --cpus-per-task=4   # maximum CPU cores per GPU request: 6 on Cedar, 16 on Graham.
#SBATCH --mem=50000M        # memory per node
#SBATCH --time=00-00:45     # time (DD-HH:MM)
#SBATCH --output=out%N-%j_tf_.out  # %N for node name, %j for jobID
#SBATCH --array=1-100

module load nixpkgs/16.09  gcc/5.4.0 gmtk python/3.8.0
source ~/py38/bin/activate

stdev=$1

(cd ./data; mkdir ./data_stdev${stdev}/)
(cd ./data; rm -r ./data_stdev${stdev}/tmp${SLURM_ARRAY_TASK_ID})

#parameters: sigma(normal dist), alpha (beta dist), beta (beta dist), run number
(cd ./data; python generate_data.py $stdev $SLURM_ARRAY_TASK_ID)

#create genomedata archive: name of input track1, "" track2, name of output archive, run number
(cd ./data; ./make-genomedata.sh test_track1.bedgraph test_track2.bedgraph tracks.genomedata $SLURM_ARRAY_TASK_ID $stdev)
(cd ./data; ./make-genomedata.sh test_track2.bedgraph test_track1.bedgraph swap_tracks.genomedata $SLURM_ARRAY_TASK_ID $stdev)
(cd ./data; ./make-genomedata.sh rev_test_track1.bedgraph rev_test_track2.bedgraph rev_tracks.genomedata $SLURM_ARRAY_TASK_ID $stdev)

SEGWAY_RAND_SEED=$SLURM_ARRAY_TASK_ID

#parameters: name of input file, name of hic file; names of output directories for segway train, identify, posterior; run number
(cd ./segway; mkdir ./out${stdev};)
(cd ./segway; ./run.sh tracks.genomedata ./out${stdev}/traindir ./out${stdev}/posteriordir $SLURM_ARRAY_TASK_ID $stdev)
(cd ./segway; ./run.sh swap_tracks.genomedata ./out${stdev}/swap_traindir ./out${stdev}/swap_posteriordir $SLURM_ARRAY_TASK_ID $stdev)
(cd ./segway; ./run.sh rev_tracks.genomedata ./out${stdev}/rev_traindir ./out${stdev}/rev_posteriordir $SLURM_ARRAY_TASK_ID $stdev)

#segway parameters: name of input file; names of output directories for segway train, identify, posterior; run number

for WEIGHT in 0 1 10 100
do
  BETA=75
  (cd ./segway-gbr/segway_gbr; mkdir ./out${stdev};)
  (cd ./segway-gbr/segway_gbr; ./run.sh tracks.genomedata "test_beta${BETA}.hic" ./out${stdev}/TRAINDIR_W${WEIGHT}_B${BETA}_ ./out${stdev}/POSTDIR_W${WEIGHT}_B${BETA}_ $SLURM_ARRAY_TASK_ID $stdev $WEIGHT $BETA)
  (cd ./segway-gbr/segway_gbr; ./run.sh swap_tracks.genomedata "test_beta${BETA}.hic" ./out${stdev}/SWAP_TRAINDIR_W${WEIGHT}_B${BETA}_ ./out${stdev}/SWAP_POSTDIR_W${WEIGHT}_B${BETA}_ $SLURM_ARRAY_TASK_ID $stdev $WEIGHT $BETA)
  (cd ./segway-gbr/segway_gbr; ./run.sh rev_tracks.genomedata "rev_test_beta${BETA}.hic" ./out${stdev}/REV_TRAINDIR_W${WEIGHT}_B${BETA}_ ./out${stdev}/REV_POSTDIR_W${WEIGHT}_B${BETA}_ $SLURM_ARRAY_TASK_ID $stdev $WEIGHT $BETA)
done
