import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "pysuchsel",
	packages = setuptools.find_packages(),
	version = "0.0.1",
	license = "gpl-3.0",
	description = "Native Python library to create and edit SVG documents",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/pysuchsel",
	download_url = "https://github.com/johndoe31415/pysuchsel/archive/v0.0.1.tar.gz",
	keywords = [ "puzzle", "crossword", "suchsel" ],
	install_requires = [
		"pysvgedit>=0.0.4",
	],
	entry_points = {
		"console_scripts": [
			"pysuchsel = pysuchsel.__main__:main",
		]
	},
	include_package_data = True,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
	],
)
