.PHONY: all commit add format_code
line_width := 120

all:
	$(MAKE) -C . commit


commit:
	$(MAKE) -C . format_code
	git commit -a


add:
	$(MAKE) -C . format_code
	git add .


format:
	# fixes imports broken by black
	isort -e -j 4 -rc -w $(line_width) .

	black -t py36 -l $(line_width) .
