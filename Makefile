IMAGE ?= vidhoarder

.PHONY: build run upgrade

build:
	@docker build -t $(IMAGE):latest .

run:
	@docker run -d --restart unless-stopped --env-file=./.env --name $(IMAGE) $(IMAGE):latest

upgrade:
	@which pip-compile > /dev/null && pip-compile -U || echo "pip-tools not installed"
