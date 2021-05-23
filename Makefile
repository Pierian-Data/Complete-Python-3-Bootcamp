serve:
	@docker container run --rm \
		-p 8888:8888 \
		--user root \
		-e NB_GID=100 \
		-v "$$PWD:/home/jovyan/work" \
		-it --name jupyter jupyter/base-notebook \
