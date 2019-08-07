from .config import *
from .helpers import create_dir

class Batch:
    def __init__(self, name, memory, log_path, timelimit='96:00:00', partition='normal', account='nn9447k'):
        self.name   = name
        self.memory = memory 
        self.log_path  = log_path
        self.timelimit = timelimit
        self.partition = partition
        self.account   = account
        self.batch_string = ''

    def head(self):
        head_string = f"""#!/bin/sh

#SBATCH -t {self.timelimit}
#SBATCH -n 1
#SBATCH -J "{self.name}"
#SBATCH --mem-per-cpu={self.memory} --partition={self.partition}
#SBATCH --account={self.account}
#SBATCH --output={self.log_path}/{self.name}-%j.out

source ~/.bashrc

module purge
module load gcc
        """
        return head_string
    def train_udpipe(self, model_path, train_data_path):
        command_string = f"""
srun udpipe --train \\
    --tagger \\
    --tokenizer {model_path} {train_data_path}"""
        self.batch_string = self.head() + command_string
        self.save_batchstring(path=os.path.join(BATCHFILES, 'latest_train_udpipe.sh'))

    def tokenize(self, model_path, input_path, output_file):
        command_string = f"""
srun /projects/nlpl/software/udpipe/latest/bin/udpipe --tokenize --tag {model_path} {input_path} > {output_file}
        """
        self.batch_string = self.head() + command_string
        self.save_batchstring(path=os.path.join(BATCHFILES, 'latest_tokenize.sh'))

    def save_batchstring(self, path):
        with open(path, 'w') as f:
            f.write(self.batch_string)

    def submit(self):
        batch_path = os.path.join(BATCHFILES, 'submit.sh')
        self.save_batchstring(path=batch_path)
        shell_output = os.popen(f'sbatch {batch_path}').read() # getting output
        print(shell_output)
        job_id = shell_output.split()[-1]                      # extract job id

        batch_history_dir = os.path.join(BATCHFILES, 'history')
        create_dir(batch_history_dir)

        batch_history_path = os.path.join(batch_history_dir, f"{job_id}.sh")
        self.save_batchstring(batch_history_path)

        print(f'Batchfile location: {batch_history_path}')
