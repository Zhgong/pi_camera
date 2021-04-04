# pi_camera
Controlling camera on raspberry pi

> `sudo apt install -y gpac`

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

