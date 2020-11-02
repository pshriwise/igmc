from setuptools import setup

kwargs = {
    'name': 'py-iga',
    'version': '0.0.1',
    'packages': ['py_iga'],

    # Metadata
    'author': 'Patrick Shriwise',
    'author_email': 'pshriwise@gmail.com',
    'description': 'Experimentation with isogeometrics for Monte Carlo particle transport',
    'url': 'https://github.com/pshriwise/py-iga',
    'download_url': 'https://github.com/pshriwise/py-iga',
    'project_urls': {
        'Issue Tracker': 'https://github.com/pshriwise/py-iga/issues',
        'Source Code': 'https://github.com/pshriwise/py-iga',
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    # Dependencies
    'python_requires': '>=3.5',
    'install_requires': [
        'openmc>0.11.0', 'numpy', 'matplotlib'
    ],
    'extras_require': {
        'test' : ['pytest', 'pytest-qt'],
        'vtk' : ['vtk']
    },
}

setup(**kwargs)
