<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Problematic Areas Detection

This module detects problematic areas of a field and extracts their location based on a given vegetation index of the examined field region. As problematic are considered areas with lowest index values.

![areas](https://user-images.githubusercontent.com/26482319/114700280-01d73380-9d2a-11eb-891f-8ee0f4e47593.jpg)


## How to run
```
python3 areas_dection.py ~IMAGE_PATH ~PROJECT_PATH ~IMAGES_DIR_PATH
```
  
The ```~IMAGE_PATH``` corresponds to the absolute path of the the examined field region and the ```~PROJECT_PATH``` to the absolute path of the folder where the extracted results of the vegetation indices and their corresponding ```*.npy``` files are saved from the ```Vegetation Indices``` module. The ```~IMAGES_DIR_PATH``` refers to the absolute path of the folder which contains the collected images from the coverage mission of the UAV.
  
> Note: This module is based on the ```*.npy``` files of ```Vegetation Indices``` module. 
  
  
## Dependencies 
Install all the neccecary dependencies using ```pip3 install <package name>```
  
Required packages:
  * opencv-python
  * numpy
  * scipy  
  * skimage
  * exif 
  * json
  * matplotlib
  * scikit-learn
  * gdal

## How to install [GDAL](https://gdal.org)
* On Linux, GDAL binary and Python binding are available through ubuntugis repository. 
  
```sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable```
  
```sudo apt-get install gdal-bin```
  
```sudo apt-get install python3-gdal```
  
  
* On Windows, the most easiest way to install GDAL Python Binding is to use the packages build by Christoph Gohlke and available [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). The ```*.whl``` package file contains a stand alone GDAL installation including all needed files (binaries, libraries, Python 
binding, etc.). After downloading the correct version of ```*.whl``` package based on the python version is installed on the operating system, install the wheel file with the following command:

```
~PATH_TO_WHL_PACKAGE python.exe -m pip install GDAL-X.X.X-cpXX-cpXXm-win_amd64.whl
```
  
To finalize the installation, it's necessary to define a new Windows environment variables named GDAL_DATA pointing the directory ```C:\Program Files\GDAL\gdal-data``` and PROJ_LIB pointing ```C:\Program Files\GDAL\projlib```.

  
## Results
The results are ```*.json``` files (one for every vegetation index) which contain all the necessary information about the centers of the detected problematic areas and the name of the nearest captured image of the UAV with their corresponding visualizations.
  
Example of a ```*.json``` file (2 detected centers)
```
  [
    {
        "Lat": XXX,
        "Lon": XXX,
        "Nearest_image": "XXX.jpeg"
    },
    {
        "Lat": XXX,
        "Lon": XXX,
        "Nearest_image": "XXX.jpeg"
    }
]
```
  
## Citation
(not published yet)
