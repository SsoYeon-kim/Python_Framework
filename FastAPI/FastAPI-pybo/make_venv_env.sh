#!/bin/bash

rm -rf migrations
rm -rf myapi
rm -rf venvs
rm  myapi.db

sudo apt update
sudo apt install python3-venv

mkdir venvs
cd venvs
python3 -m venv myapi
cd myapi/bin
source activate

cd ../../../
pip install wheel
pip install -r requirements.txt

alembic init migrations

cd migrations
sed -i '1 i\import models\ntarget_metadata = models.Base.metadata' env.py
sed -i '/target_metadata = None/d' env.py
cd ../

alembic revision --autogenerate
alembic upgrade head
