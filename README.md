# Systemd (Linux):
You can create a systemd service to manage your script as a background service.

## Create a new service file:

### bash
```
sudo nano /etc/systemd/system/bot.service
```

Add the following configuration, adjusting the User, WorkingDirectory, and ExecStart fields as needed:`

### makefile
```
[Unit]
Description=Bot Service
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/your/bot/directory
ExecStart=/usr/bin/python3 /path/to/your/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and exit the file. Then, run the following commands to enable and start the service:


### bash
```
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service
```

To check the status of your service, use sudo `systemctl status bot.service`.