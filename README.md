# harrymd/NormalModes

This repository is a fork of [Jia Shi's *NormalModes*](https://github.com/js1019/NormalModes) code. It is mostly the same, but with a few customised wrapper scripts.

## Compilation

Follow the instructions in `INSTALL.md`. Run `make` in the `src/` directory.

## Keeping scripts synchronised

Scripts are stored in `/work/06414/tg857131/NormalModes/` and `/Users/hrmd_work/Documents/research/stoneley/code/NormalModes`. If you make changes to these scripts in either environment, use `git` to synchronise them.

## Building the model

Follow the instructions at [my fork of Jia's *PlanetaryModels* code](https://github.com/harrymd/PlanetaryModels).

## Submitting job to cluster

Once the input model has been built,

```bash
cd /work/06414/tg857131/NormalModes/bin
python3 make_run_files.py
```

to create the output directory in `/scratch`, copy across the input files, and prepare the `.sbatch` script. You should edit `make_run_files.py` to change the number of nodes, requested computational time, queue name, or other settings. Then submit the job:

```bash
cd /scratch/06414/tg857131/NormalModes/output/name_of_job
sbatch run_normal_modes.bash
```

## Storing output files

To copy the output files from the cluster to the hard disk, use

```bash
rsync -rvh tg857131@stampede2.tacc.utexas.edu:/scratch/06414/tg857131/NormalModes/output/ /Volumes/stoneley5TB/all/NormalModes/v2
```

To send them to the local machine, you can use

```bash
rsync -rvh tg857131@stampede2.tacc.utexas.edu:/scratch/06414/tg857131/NormalModes/output/ /Users/hrmd_work/Documents/research/stoneley/output/NormalModes
```

but these files are often large so it may be better to avoid this
