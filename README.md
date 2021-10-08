<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Problematic Areas Detection

This module detects problematic areas of a field and extracts their location based on a given vegetation index of the examined field region. As problematic are considered areas with lowest index values.

![areas](https://user-images.githubusercontent.com/26482319/114700280-01d73380-9d2a-11eb-891f-8ee0f4e47593.jpg)


## How to run
```
python3 areas_dection.py ~IMAGE_PATH ~FOLDER_PATH ~IMAGES_DIR_PATH
```

  

## Dependencies 
Install all the neccecary dependencies using ```pip3 install <package name>```
  
Required packages:
  * opencv-python
  * numpy
  * scipy  
  * skimage
  * exif 
  * json
  * pandas  
  * sklearn 
  * sklearn
  * gdal

## How to install [GDAL](https://gdal.org)
  On Linux, GDAL binary and Python binding are available through ubuntugis repository
  
  
  On Windows, the most easiest way to install GDAL Python Binding is to use the packages build by Christoph Gohlke and available [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). The ```*.whl``` package file contains a stand alone GDAL installation including all needed files (binaries, libraries, Python 
binding, etc.). After downloading the correct version of .whl package based on the python version is installed on the operating system, install the wheel file:

```
~PATH_TO_WHL_PACKAGE python.exe -m pip install GDAL-X.X.X-cpXX-cpXXm-win_amd64.whl
```
To finalize the installation, it's necessary to define a new Windows environment variables named GDAL_DATA and pointing the directory ```C:\Program Files\GDAL\gdal-data``` and PROJ_LIB pointing ```C:\Program Files\GDAL\projlib```.
  
  
## Citation
(not published yet)
