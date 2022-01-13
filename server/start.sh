pid=`sudo netstat -tpln | grep ':80' | awk '{split($7, list, "/"); print list[1]}'`
echo $pid
sudo kill $pid
sudo -S python3.8 server.py
