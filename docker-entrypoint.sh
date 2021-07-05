#!/bin/sh

MODE=$1
echo "docker-entrypoint.sh executing ..."

echo "##### Input ######"
printf "Container Mode: [%s]\n" $MODE
echo "##################"
echo ""

if [ $MODE = "Server" ]; then
    echo "Start Server"
    python3 ./server.py
else
    echo "Start Server"
    python3 ./server.py
fi

echo ""
echo "##################"
echo "Finished!"
