from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in rabbitmq_message_publish/__init__.py
from rabbitmq_message_publish import __version__ as version

setup(
	name="rabbitmq_message_publish",
	version=version,
	description="App for publishing doctype insert/update/delete messages to Rabbit MQ",
	author="Hotset",
	author_email="jfinke@hotset.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
