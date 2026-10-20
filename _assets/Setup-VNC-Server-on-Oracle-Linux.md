# Setup VMC Server on Oracle Linux 

```bash
sudo dnf group install -y "Server with GUI"

sudo systemctl set-default graphical
sudo dnf upgrade -y
sudo dnf install -y tigervnc-server tigervnc-server-module
```
Choose the conneciton password
```bash
vncpasswd
```

Configure vnc service
```bash
echo ":1=$(whoami)"| sudo tee -a /etc/tigervnc/vncserver.users > /dev/null
printf 'session=gnome\ngeometry=1920x1080' | sudo tee -a /etc/tigervnc/vncserver-config-defaults > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now vncserver@:1.service
```

Check the service
```bash
sudo systemctl status vncserver@:1.service
sudo systemctl enable vncserver@:1.service
sudo systemctl restart vncserver@:1.service
```
configure tigervnc
```bash
sudo vi /etc/tigervnc/vncserver-config-defaults
geometry=1920x1080
```

Create SSL Tunnel
```bash
ssh -L 5901:localhost:5901 -i ${YOUR_KEY} opc@bastion
```

