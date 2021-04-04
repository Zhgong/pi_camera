# 首次运行执行次脚本
# Install the service with systemctl
sudo ln -s /home/pi/pi_camera/service/cameraeye.service /etc/systemd/system

sudo systemctl enable  cameraeye

sudo systemctl start  cameraeye