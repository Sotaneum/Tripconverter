from setuptools import setup, find_packages

setup(name='tripconverter',
      version='0.0.1',
      url='https://github.com/Sotaneum/2019-Molit',
      license='MIT',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='eTAS(TRIP) to data',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md', encoding='UTF8').read(),
      zip_safe=False
	  )