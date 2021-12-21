.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  allocate to build and deploy a workshop cluster"
	@echo "  destroy  to tear down a workshop cluster"

.PHONY: allocate
allocate:
	ansible-playbook \
		-i inventory \
		--extra-vars 'ssl_cert_dir=${SECRETS}/certs/qiime2.org' \
		playbooks/aws-workshop-allocate.yml

.PHONY: destroy
destroy:
	ansible-playbook \
		-i inventory \
		playbooks/aws-workshop-destroy.yml
