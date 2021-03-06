import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'mongoengine',
    'pycrypto',
    'boto',
    'dateutils'
    ]

setup(name='nokkhum-api',
      version='0.0',
      description='nokkhum-api',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="nokkhumapi",
      entry_points = """\
      [paste.app_factory]
      main = nokkhumapi:main
      [console_scripts]
      initialize_nokkhum_db = nokkhumapi.scripts.initializedb:main
      """,
      )

