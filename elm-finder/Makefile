.PHONY: all commit add format
line_width := 120

all:
	$(MAKE) -C . commit


commit:
	$(MAKE) -C . format
	git commit -a


add:
	$(MAKE) -C . format
	git add .


format:
	# fixes imports broken by black
	isort -e -j 4 -rc -p libs -w $(line_width) .

	black -t py36 -l $(line_width) .
