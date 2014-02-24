#/usr/bin/env bash
py.test -x -s datadjables --cov-report html --cov datadjables


# coverage html # --omit='*datadjable_testing*'

open htmlcov/index.html





#py.test -s -x -n 4 exams main candidates curriculum csvutils scansheets rooms documents questions -x -s --tb=short \
#	&& coverage html --omit='*tests*,*django_finnegan*,*management*,*browsertests*,*settings*,*py.test*,*main/wsgi*,*main/utils*,*documents/utils/*' \
#	&& open htmlcov/index.html

