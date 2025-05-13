IMAGE ?= vidhoarder

.PHONY: build clean run upgrade

build:
	@docker build  --target=prod -t $(IMAGE):latest .

clean:
	docker rm -f $(IMAGE) || true

run:
	@docker run -d --restart unless-stopped --env-file=./.env --name $(IMAGE) $(IMAGE):latest

upgrade:
	@command uv --version >/dev/null 2>&1 && uv lock -U || echo "uv not installed"
