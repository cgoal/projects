# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.core import Extension
from Cython.Build import cythonize

extensions=[Extension('faceDetect',['faceDetect.py']),Extension('fr_mp',['fr_mp.py'])]
#setup(ext_modules=cythonize('faceDetect.py'))
setup(ext_modules=cythonize(extensions))