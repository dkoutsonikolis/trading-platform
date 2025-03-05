run:
	docker-compose up -d --build

teardown:
	docker-compose down -v

recreate: teardown run

test:
	docker-compose exec web pytest ${path}

.PHONY: \
	run \
	teardown \
	recreate \
	test \
