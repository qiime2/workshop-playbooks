# QIIME 2 Workshop Galaxy Server

This set of playbooks is heavily based on:

https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible-galaxy/tutorial.html

## Quickstart

1. Allocate an EC2 instance in the region of your choice, with the latest
   Ubuntu distro (note, you'll probably need to set up a VPC for this;
   alternatively you could allocate an AWS Lightsail instance):
    - `m4.16xlarge` works for mid-size workshops (TODO: verify this)
    - Make sure to provision an EBS volume (1000 GB works for mid-size workshops)
    - Provision with a public-facing IP address
    - Create a new SSH keypair, if necessary and associate it with this instance.
1. Set up DNS (create/update an `A` record with the new IP, at the domain you
   want (like workshop-server.qiime2.org)
1. `touch galaxy/.vault-password.txt` and add the vault secret (as Evan or Matt
   for help with this).
1. Edit `hosts` (set domain from above; ssh key location)
1. Copy SSL certs from caporaso-lab secrets:

       cp ~/projects/qiime2/caporaso-lab-secrets/certs/qiime2.org/\*.qiime2.org.chained.crt files/ssl/fullchain.pem
       cp ~/projects/qiime2/caporaso-lab-secrets/certs/qiime2.org/\*.qiime2.org.key files/ssl/privkey.pem

1. Create conda env (important, the tool definitions step below _must_ be run
   on a linux host):

       # Change this step to meet your needs (a custom workshop distro, staging release, etc)
       wget https://raw.githubusercontent.com/qiime2/environment-files/master/latest/staging/qiime2-latest-py38-linux-conda.yml
       conda env create -n workshop-server --file qiime2-latest-py38-linux-conda.yml
       conda install -n workshop-server -c conda-forge ansible rsync
       rm qiime2-latest-py38-linux-conda.yml
       conda activate workshop-server
       pip install bioblend

1. Install ansible roles:

       ansible-galaxy install -p roles -r requirements.yml

1. Build q2galaxy tool definitions:

       q2galaxy template all files/tools/
       q2galaxy template tool-conf /opt/qiime2_tools/tools files/tools/qiime2_tool_conf.xml

1. Run the playbook:

       ansible-playbook galaxy.yml

1. You might need to log into the server and restart the galaxy instance:

       sudo systemctl restart galaxy
       sudo systemctl status galaxy
       journalctl -fu galaxy

1. You'll need to manually create the first admin user account (in a local
   python session):

       from bioblend.galaxy import GalaxyInstance

       gi = GalaxyInstance('https://workshop-server.qiime2.org', key='GET THIS FROM THE VAULT')
       gi.users.create_local_user('my first admin user', 'their email', 'initial password')

1. Run the playbook one last time:

       ansible-playbook galaxy.yml
