.PHONY: all debug minify format build_prod
elm_files := $(wildcard src/*.elm)
base_source := src/Main.elm
js_output := ../elm-finder/static/js/elm-main.js
compiled_js := ../elm-finder/static/js/elm-compiled.js



all: $(elm_files)
	$(MAKE) -C . debug


minify: $(js_output)
	uglifyjs $(js_output) --compress 'pure_funcs="F2,F3,F4,F5,F6,F7,F8,F9,A2,A3,A4,A5,A6,A7,A8,A9",pure_getters,keep_fargs=false,unsafe_comps,unsafe' | uglifyjs --mangle --output=$(compiled_js)


production: $(elm_files)
	$(MAKE) -C . format
	elm make $(base_source) --optimize --output=$(js_output)
	$(MAKE) -C . minify

debug: $(elm_files)
	elm make $(base_source) --debug --output=$(compiled_js)
	$(MAKE) -C . format


test: $(elm_files)
	elm make $(base_source) --output=$(compiled_js)


format: $(elm_files)
	elm-format --yes src/
