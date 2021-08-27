-include .python-Makefile

.PHONY: init
init:
	@curl -fsL https://github.com/bonjoursoftware/build-tools/raw/main/python/Makefile > .python-Makefile || rm .python-Makefile
	@test -s .python-Makefile || (echo "Unable to download base Makefile, is this machine online?"; exit 1)
	@echo "Init successful, run make again to list the available make targets"
