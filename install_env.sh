

#wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
#bash Miniconda2-latest-Linux-x86_64.sh -b -p miniconda

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p miniconda

echo "Writing into pn.env"

echo ". $(pwd)/miniconda/etc/profile.d/conda.sh" >> pn.env
echo "conda activate base" >> pn.env
echo "export PROJECT=""$(pwd)" >> pn.env
echo ""
echo "module load gcc "
#echo "module load python3/3.7.0.gnu"

. miniconda/etc/profile.d/conda.sh

mkdir software
cd software

mkdir bin
BIN_DIR="$(pwd)/bin"

conda activate base
#pip install dynet

git clone https://github.com/maxtrem/uuparser
pip install -r uuparser/requirements.txt
pip install --ignore-installed opustools-pkg
#conda create -n py37 python=3.7 -y
#conda activate py37
module purge
module load gcc

pip install numpy
git clone https://github.com/robertostling/eflomal
cd eflomal
make 
install -t $BIN_DIR eflomal
python setup.py install


echo "Envoroment installation script finished. Use 'source pn.env' to activate."