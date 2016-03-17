from distutils.core import setup

setup(
    name='StageIndicateursMultiDispositifs',
    version='1.0',
    packages=['Dev', 'Dev.src'],
    url='',
    license='',
    author='Valentin Lachand',
    author_email='valentin@lachand.net',
    description='',
    install_requires=[
          'kivy', 'demjson', 'plotly', 'shapely'
      ]
)
