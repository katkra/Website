# Website


#run elasticsearch
c:\elasticsearch-7.12.0\bin\elasticsearch-service.bat install
c:\elasticsearch-7.12.0\bin\elasticsearch-service.bat start

Create a virtual environment in which to run it in. ->https://www.c-sharpcorner.com/article/steps-to-set-up-a-virtual-environment-for-python-development/

.\virtual\Scripts\activate

(virtual) set FLASK_APP=web.py
(virtual) set MS_TRANSLATOR_KEY=
(virtual) flask run
