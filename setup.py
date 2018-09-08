import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

AUTHORS = [
    ('Evan Biederstedt', 'evan.biederstedt@gmail.com'),
    ('Tze Yin Lim', 'tl2829@columbia.edu'),
    ('Peng Zhang', 'pzhang@rockefeller.edu'),
    ('Naina Thangaraj', 'nthangaraj@dnanexus.com'),
    ('Kundai Andrew Midzi', 'kundai.andrew.midzi@gmail.com'),
    ('Kelly Terlizzi', 'kelly.terlizzi@mdrc.org')
]

def _list_authors(authors=AUTHORS):
    def _sort_by_surname(record):
        # This is naive, but...
        name = record[0]
        sname = name.split(' ')[-1]
        return sname

    for name, email in sorted(authors, key=_sort_by_surname):
        yield '{name} <{email}>'.format(name=name, email=email)

def _get_authors_str():
    return ', '.join(list(_list_authors()))

# TODO(zeroslack): use setuptools_scm
setuptools.setup(
    name='expressivar',
    version='0.0.2',
    author=_get_authors_str(),
    author_email='https://ncbi-hackathons.github.io/',
    description='Package to determine mutations from expressed genes',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NCBI-Hackathons/ExpressiVar',
    packages=setuptools.find_packages(),
    keywords='SNPs RNA-Seq VCF',
    install_requires=['wrapt', 'pyvcf'],
    include_package_data=True,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ),
)
