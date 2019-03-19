import sys
#import oyaml, ruamel.yaml
import oyaml

from oyaml import load, dump

DOCUMENTATION = '''
---
module: buildahr
version_added: historical
short_description: Creates an Ansible Playbook from a simpler YAML file:
     -  <add more here>:

# informational: requirements for nodes
requirements: [ buildah, libselinux-python ]
author:
    - "Red Hat"
    - "William Henry"
'''

EXAMPLES = '''

  - name: BUILDAHR | Generate ansible-buildah playbook "buildahr <buildahbook.yml>" command
	image:
	  name: myfedorapy
	  from: quay.io/fedora:latest
	  packages: python
	  copy: library/buildahr.py /tmp
 	  config:
	    author: ipbabble
	  cmd: python --version

  - debug: var=result.stdout_lines

'''

class Buildahfrom(object):
	yaml_tag = '- name: BUILDAH - start the new image from'

	def __init__(self, image):
		self.buildah_from = { 'name': image}
		self.register = 'from_result'

	@classmethod
	def to_yaml(cls, representer, node):
		return representer.represent_scalar(cls.yaml_tag,
											u'{buildah_from} {register}'.format_map(vars(self)))

	@classmethod
	def from_yaml(cls, constructor, node):
		return cls(*node.value.split('\n'))

class Buildahmount(object):
	yaml_tag = '- name: BUILDAH - mount the contianer file system'

	def __init__(self):
		self.buildah_mount = { 'name': "{{ from_result.stdout | trim }}" }
		self.register = 'mount_result'


class DNFonmount(object):
	yaml_tag = '- name: DNF - install direct into mount'

	def __init__(self, packages):
		self.dnf = { 'name': packages, 
					 'installroot': "{{ mount_result.stdout | trim }}",
					 'relserver': 29, 
					 'state': "latest" }
		self.register = 'dnf_result'


class Buildahrun(object):
	yaml_tag = '- name: BUILDAH - run a command in the container'

def __init__(self, command):
		self.buildah_run = { 'cmd': command }




def main():

	with open("buildahbook.yml", "r") as buildahbook:
		try:
			buildahyaml = oyaml.safe_load(buildahbook)
		except oyaml.YAMLError as ymlexcp:
			print(ymlexcp)
	try:
		print oyaml.dump(buildahyaml)
	except oyaml.YAMLError as ymlexcp:
		print(ymlexcp)

	playbook = dict()
	playbook['tasks'] = list()


	with open('buildah_playbook.yml', 'w') as outfile:
		from_image = buildahyaml['image']['from']
		print(from_image)
	   	oyaml.dump([Buildahfrom(from_image)], sys.stdout, default_flow_style=False)
	   	oyaml.dump([Buildahmount()], sys.stdout, default_flow_style=False)
	   	oyaml.dump([DNFonmount(buildahyaml['image']['packages'])], sys.stdout, default_flow_style=False)

if __name__ == '__main__':
    main()	
    