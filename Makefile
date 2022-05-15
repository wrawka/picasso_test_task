build:
	docker build . -t parser:sample
run:
	docker run --rm -it -p 8000:8000/tcp parser:sample