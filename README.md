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
  
  On Windows, the most easiest way to install GDAL Python Binding is to use the packages build by Christoph Gohlke and available here. 

## Citation
(not published yet)
