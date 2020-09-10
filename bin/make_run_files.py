import os
from shutil import copyfile

dir_scratch = '/scratch/06414/tg857131/'
dir_work = '/work/06414/tg857131/'
dir_NM = os.path.join(dir_work, 'NormalModes')
dir_NM_output = os.path.join(dir_scratch, 'NormalModes', 'output')
dir_NM_input = os.path.join(dir_scratch, 'PlanetaryModels', 'output', 'LLSVP')

def make_config_file(JOB, freq_low, freq_upp, str_input):

    # Set base of name of model input files.
    name_base = 'mod.1'
    
    # Choose whether to use a CG Method (True or False).
    CGMethod = True
    if CGMethod:

        str_CGMethod = '.TRUE.'

    else:

        str_CGMethod = '.FALSE.'

    # Define input and output directory.
    # Extract order of finite element basis from model name.
    pOrder = int(str_input[-1])
    dir_input = os.path.join(dir_NM_input, str_input)
    name_output = '{}_{:05.2f}_{:05.2f}_{:1d}'.format(str_input, freq_low, freq_upp, JOB)
    dir_output = os.path.join(dir_NM_output, name_output)

    # Prepare the lines of the configuration file.
    lines = [
        'JOB = {:1d}'.format(JOB),
        'CGMethod = {}'.format(str_CGMethod),
        'lowfreq = {:.2f}'.format(freq_low),
        'upfreq = {:.2f}'.format(freq_upp),
        'pOrder = {:1d}'.format(pOrder),
        'inputdir = {}/'.format(dir_input),
        'outputdir = {}/'.format(dir_output),
        'basename = {}'.format(name_base)]

    # Write the configuration file.
    file_config = 'global_conf'
    with open(file_config, 'w') as out_id:

        for line in lines:

            out_id.write('{}\n'.format(line))

    return dir_input, dir_output, file_config

def make_sbatch_file(queue, nodes, ntasks_per_node, time_str, dir_input, dir_output, allocation = 'XX=XXX012345', mail_user = 'name@gmail.com'):

    # Write the sbatch file.
    lines = [
            '#!/bin/bash',
            '#SBATCH -J LLSVP',
            '#SBATCH -o LLSVP_%j.txt',
            '#SBATCH -e LLSVP_%j.err',
            '#SBATCH -p {}'.format(queue),
            '#SBATCH --nodes={:d}'.format(nodes),
            '#SBATCH --ntasks-per-node={:d}'.format(ntasks_per_node),
            '#SBATCH --export=ALL',
            '#SBATCH --time={}'.format(time_str),
            '#SBATCH -A {}'.format(allocation),
            '#SBATCH --mail-user={}'.format(mail_user),
            '#SBATCH --mail-type=all',
            '',
            'export OMP_NUM_THREADS=2',
            'export MV2_ENABLE_AFFINITY=0',
            '',
            'source {}'.format(os.path.join(dir_NM, 'SetEnv')),
            'cd {}'.format(dir_output),
            '',
            'jid=$(echo $SLURM_JOB_ID)',
            'outfile=\'LLSVP_\'$jid\'.txt\'',
            'errfile=\'LLSVP_\'$jid\'.err\'',
            '',
            '# These lines throttle the rate of I/O.',
            'module use /work/01255/siliu/stampede2/ooops/modulefiles/',
            'module load ooops',
            'export IO_LIMIT_CONFIG=/work/01255/siliu/stampede2/ooops/1.0/conf/config_low',
            'set_io_param 0 low',
            'set_io_param 1 low',
            'set_io_param 2 low',
            '',
            'ibrun {}'.format(os.path.join(dir_NM, 'bin', 'plmvcg_stampede2.out')),
            '']
            #'cp {}/bin/$outfile {}'.format(dir_NM, dir_output),
            #'cp {}/bin/$errfile {}'.format(dir_NM, dir_output)]#,
            #'',
            #'# This line reduces I/O by copying Python libraries to a temporary directory.',
            #'export rt LD_PRELOAD=/work/00410/huang/share/patch/myopen.se /work/01255/siliu/stampede2/ooops/modulefiles/',
            #'',
            #'python3 /work/06414/tg857131/mode_postprocess/process.py {} {}'.format(dir_input, dir_output),
            #'',
            #'cp {}/bin/$outfile {}'.format(dir_NM, dir_output),
            #'cp {}/bin/$errfile {}'.format(dir_NM, dir_output)]

    file_sbatch = 'run_normal_modes.bash'
    with open('run_normal_modes.bash', 'w') as out_id:

        for line in lines:

            out_id.write('{}\n'.format(line))

    return file_sbatch

def main():

    # Choose JOB variable.
    # 1 without gravity.
    # 2 with gravity.
    JOB = 1

    # Set lower and upper frequency limits (in mHz).
    freq_low = 0.1
    freq_upp = 1.0

    # Define input and output directory name.
    str_input ='prem_0439.4_2.00_1'

    # Write the config file.
    dir_input, dir_output, file_config = make_config_file(JOB, freq_low, freq_upp, str_input)

    # Define the cluster variables.
    queue = 'skx-normal'
    nodes = 1 
    ntasks_per_node = 48
    time_str = '00:20:00'

    # Write the sbatch file.
    file_sbatch = make_sbatch_file(queue, nodes, ntasks_per_node, time_str, dir_input, dir_output, allocation = 'TG-EAR170019', mail_user = 'hrmd@mit.edu')

    # Create the output directory and move the input files there.
    if not os.path.isdir(dir_output):

        os.mkdir(dir_output)

    for file_ in [file_config, file_sbatch]:

        copyfile(file_, os.path.join(dir_output, file_))

if __name__ == main():

    main()
