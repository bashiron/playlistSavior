#!/bin/bash
#logfile='/var/log/playlist_savior.log'
logfile='/home/bashiron/playlist_savior.log'
cd /home/bashiron/bashi/projects/youtubePlaylistSavior
source .venv/bin/activate
echo '---' >> $logfile
date >> $logfile
echo >> $logfile
python src/main.py 2>&1 | tee -a $logfile
# trim the log
flock logfile ./trim.sh logfile
deactivate
exit
