SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = forge
SOURCEDIR     = docs
BUILDDIR      = docs/build
MANAGE_COMMAND = python manage.py

run:
	python manage.py runserver

test_watch:
	find **/*.py | entr make test_unit

test_cov:
	rm -r htmlcov 2>/dev/null; true
	$(MANAGE_COMMAND) test -- --cov=. --cov-report html

test_unit:
	$(MANAGE_COMMAND) test

lint:
	pylint forge

types:
	mypy forge

graph:
	$(MANAGE_COMMAND) graph_models -X User,LogEntry,ContentType,AbstractUser,Group,Permission,Session,AbstractBaseSession -g -o docs/_static/models.png forge
	pyreverse -m y -p forge -o png --ignore=migrations forge

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%:
	$(MANAGE_COMMAND) $@
