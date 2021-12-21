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

### Configure

Edit `group_vars/all`, paying attention to comment out the test config:

```
# TESTING CONFIG
jump_host_type: t3.small
compute_host_type: t3.nano
compute_host_count: 1
volume_size: "8"
```

and uncomment the production config:

```
# PRODUCTION CONFIG
# jump_host_type: m5.8xlarge
# compute_host_type: m5.2xlarge
# compute_host_count: 12
# volume_size: "50"
```

Don't forget to edit the production config values, after uncommenting. In
general you don't need to edit the `*_host_type` entries, but you should tweak
`compute_host_count` to accomodate the expected number of active user accounts
(we often include 1-3 "spare" hosts, depending on the size of the workshop).

**Also, edit the `qiime2_release` key to match the desired QIIME 2 epoch.**

The remaining config values shouldn't generally need adjustment.

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
