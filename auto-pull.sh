#!/bin/sh

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
	echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
	echo "Need to pull"
	kill $(ps aux | grep '[S]CREEN -dmS cs408 python run.py' | awk '{print $2}'); git pull; screen -dmS cs408 python run.py
elif [ $REMOTE = $BASE ]; then
	echo "Need to push"
else
	echo "Diverged"
fi
