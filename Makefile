test:
	cd tests && ./manage.py test $1

lint:
	black check_prefetch tests noxfile.py