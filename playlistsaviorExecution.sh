#!/bin/bash
#log_dir='/var/log/playlist_savior.log'
log_dir='/home/bashiron/playlist_savior.log'
cd /home/bashiron/bashi/projects/youtubePlaylistSavior
source .venv/bin/activate
echo '---' >> $log_dir
date >> $log_dir
echo >> $log_dir
python src/main.py 2>&1 | tee -a $log_dir
deactivate
exit
