# pi_camera
Controlling camera on raspberry pi with streamlit

## How to use
```bash
$ sudo cp cameraeye.service /etc/systemd/system/
```

## run
```bash
$ sudo systemctl start cameraeye
```

## run at start up
```bash
$ sudo systemctl enable cameraeye
```

## check log
```bash
$ sudo systemctl status cameraeye
```

## Streamlit works with following system
```
Ubuntu 20.04.3 LTS
Linux ubuntu-pi-cam-211121 5.4.0-1046-raspi #50-Ubuntu SMP PREEMPT Thu Oct 28 05:32:10 UTC 2021 aarch64 aarch64 aarch64 GNU/Linux
```

## install opencv on Raspberry pi
>`sudo apt install python3-opencv`
>
>`pip install opencv-contrib-python`