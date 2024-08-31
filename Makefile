IMAGE ?= vidhoarder

.PHONY: build clean run upgrade

build:
	@docker build -t $(IMAGE):latest .

clean:
	docker rm -f $(IMAGE) || true

run:
	@docker run -d --restart unless-stopped --env-file=./.env --name $(IMAGE) $(IMAGE):latest

upgrade:
	@which pip-compile > /dev/null && pip-compile -U || echo "pip-tools not installed"
