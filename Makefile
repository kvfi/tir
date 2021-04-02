PYTHON	?= python
SETUP	:= setup.py

install:
		$(PYTHON) $(SETUP) bdist_wheel $(DESTDIR)

clean:
		$(PYTHON) $(SETUP) clean --all

uninstall: clean
		-rm -rf build dist *.egg-info

.PHONY: install clean uninstall
