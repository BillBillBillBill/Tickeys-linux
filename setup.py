from setuptools import setup, find_packages
from tickeys import __version__, __author__, __email__

requirements = [
    'Kivy',
    'evdev',
]


setup(name='tickeys',
      version=__version__,
      download_url='git@github.com:BillBillBillBill/Tickeys-linux.git',
      packages=['tickeys'],
      package_dir={'tickeys': 'tickeys'},
      include_package_data=True,
      package_data={'tickeys': ['*.*']},
      # data_files=[],
      classifiers=[
          'Intended Audience :: End Users/Desktop',
          'Development Status :: 3 - Alpha',
          'Environment :: X11 Applications',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 2.7',
      ],
      author=__author__,
      author_email=__email__,
      description='Instant audio feedback when typing. For Linux.',
      long_description=open('README.md').read(),
      keywords='keyboard typing audio feedback ',
      url='https://github.com/BillBillBillBill/Tickeys-linux',
      license='MIT',
      entry_points={
          'console_scripts': ['tickeys = tickeys:main']
      },
      install_requires=requirements,
      tests_require=requirements)
