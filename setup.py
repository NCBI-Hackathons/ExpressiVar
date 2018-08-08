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
        yield f'{name} <{email}>'

def _get_authors_str():
    return ', '.join(list(_list_authors()))

setuptools.setup(
    name='expressivar',
    version='0.0.1',
    author=_get_authors_str(),
    author_email='https://ncbi-hackathons.github.io/',
    description='Package to determine mutations from expressed genes',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NCBI-Hackathons/ExpressiVar',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
