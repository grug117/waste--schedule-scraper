#!/bin/bash

# check if no argument was passed
if [ $# -eq 0 ]; then
  echo "Error: No environment argument passed."
  exit 1
fi

conda activate $1
conda install --file requirements.txt

base_env_site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
working_dir=$(pwd)

cd $base_env_site_packages
zip -r dependencies.zip *
mv dependencies.zip $working_dir/dependencies.zip
cd $working_dir

zip -r build.zip *.py
