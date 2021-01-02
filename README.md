# Workshop Provisioning Playbooks

## Quickstart

### Prereqs

- Ansible
- conda
- AWS Account
- A domain to point the infrastructure to
- Decrypted `secrets`

### Setup

```bash
$ conda create -n workshop-prov -c conda-forge ansible boto3
$ conda activate workshop-prov
$ pip install passlib PyPDF2 reportlab
$ export SECRETS=/path/to/secrets
$ export AWS_ACCESS_KEY_ID='AK123'
$ export AWS_SECRET_ACCESS_KEY='abc123'
$ export QIIME_WORKSHOP_NAME='QIIME 2 Workshop'
$ export QIIME_EIP='1.2.3.4'
$ export QIIME_SSL_DOMAIN='workshop.example.org'
```

- `QIIME_EIP` is the AWS Elastic IP that should be associated with the jump
   host.
- `QIIME_SSL_DOMAIN` is the the configured DNS-target for the QIIME_EIP.

### Allocate infrastructure

```bash
$ make allocate
```

**Note:** When provisioning for the first time, you'll need to remove any files
that may be in the `tmp` directory (in the root of this repo) in order to
generate new user accounts. The `.gitkeep` file in `tmp` doesn't need to be
deleted.

### Destroy all infrastructure (including EBS Volumes)

```bash
$ make destroy
```
