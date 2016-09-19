while true ; do
    sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
    sleep 300
done
