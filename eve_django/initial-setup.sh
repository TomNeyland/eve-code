#!/bin/bash
echo "Setting up standard django tables"
python manage.py syncdb --database default --noinput
./download-sde-db.sh
echo "Done with initial setup"
