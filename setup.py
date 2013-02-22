try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name = 'django-flatblocks-xtd',
    version = '0.1a1',
    description = 'django-flatblocks-xtd acts like django-flatblocks but '
                  'adds support for markup content with django-markup and '
                  'inline media content with django-inline-media.',
    long_description = open('README.rst').read(),
    keywords = 'django apps',
    license = 'New BSD License',
    author = 'Daniel Rus Morales',
    author_email = 'mbox@danir.us',
    url = 'http://github.com/danirus/django-flatblocks-xtd/',
    dependency_links = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(exclude=['ez_setup', 'test_project']),
    include_package_data = True,
    zip_safe = False,
)
