FILE = camera.service
.PHONY:  help

help:
	@echo available command: install, reload, clean


install: venv service enable start

service:
	sudo ln ./camera.service /etc/systemd/system/

enable:
	sudo systemctl enable camera

start:
	sudo systemctl start camera

stop:
	sudo systemctl stop camera

venv:
	@echo making virtual enviroment ...
	virtualenv venv
	@echo install packages ...
	./venv/bin/pip install -r requirements.txt

reload:
	sudo systemctl daemon-reload
	sudo systemctl reload-or-restart camera

clean:
	rm -rf venv
	sudo rm -f /etc/systemd/system/$(FILE)
