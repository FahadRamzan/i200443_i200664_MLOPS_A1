install:
	pip3 install -r requirements.txt

docker:
	docker build -t mlops_A1 .

images:
	docker images

run:
	docker run -p 5000:5000 mlops_a1

