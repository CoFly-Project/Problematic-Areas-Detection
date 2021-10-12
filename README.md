<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Problematic Areas Detection

<!-- This module detects problematic areas of a field and extracts their location based on a given vegetation index of the examined field region. As problematic are considered areas with lowest index values. -->

The main objective of this module is to detect problematic areas of a field and extract their location based on a given vegetation index of the examined field region. As problematic are considered areas with lowest index values. 

The results of the ```Problematic Areas Detection``` module are ```*.png``` and  ```*.json``` files (one for every vegetation index). The ```*.png``` files demonstrate the points of interest of each vegetation index and the ```*.json``` files contain all the necessary information about the geolocation of these points and the name of the nearest captured image of the UAV.

  
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
* On **Linux**, GDAL binary and Python binding are available through ubuntugis repository. 
  
```sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable```
  
```sudo apt-get install gdal-bin```
  
```sudo apt-get install python3-gdal```
  
  
* On **Windows**, the most easiest way to install GDAL Python Binding is to use the packages build by Christoph Gohlke and available [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). The ```*.whl``` package file contains a stand alone GDAL installation including all needed files (binaries, libraries, Python 
binding, etc.). After downloading the correct version of ```*.whl``` package based on the python version is installed on the operating system, install the wheel file with the following command:

```
~PATH_TO_WHL_PACKAGE python.exe -m pip install GDAL-X.X.X-cpXX-cpXXm-win_amd64.whl
```
  
To finalize the installation, it's necessary to define a new Windows environment variables named GDAL_DATA pointing the directory ```C:\Program Files\GDAL\gdal-data``` and PROJ_LIB pointing ```C:\Program Files\GDAL\projlib```.

  
  
## How to run
  
1. Clone this repo
2. Open terminal on ~REPO_PATH
3. Run:
```
python3 areas_dection.py ~IMAGE_PATH ~PROJECT_PATH ~IMAGES_DIR_PATH
```
**ARGUMEΝTS**
  
  * ```~IMAGE_PATH:``` corresponds to the absolute path of the input image of the examined area
  * ```~PROJECT_PATH:``` refers to the absolute path of the folder where the extracted results of the [__Vegetation Indices__](https://github.com/CoFly-Project/Vegetation-Indices) module are saved.
  * ```~IMAGES_DIR_PATH:``` refers to the absolute path of the folder which contains the collected images from the coverage mission of the UAV.
  
  
<!-- The ```~IMAGE_PATH``` corresponds to the absolute path of the input image and the ```~PROJECT_PATH``` to the absolute path of the folder where the extracted results of the ```Vegetation Indices''' module are saved. The ```~IMAGES_DIR_PATH``` refers to the absolute path of the folder which contains the collected images from the coverage mission of the UAV. -->
  
> Note: This module is based on the ```*.npy``` files of [```Vegetation Indices```](https://github.com/CoFly-Project/Vegetation-Indices) module. 
  
  
## Results
  
  * **Visualizations**

  
  <table class="center">
   <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136773402-d76cdbea-143c-42e4-9df9-10ec277c902a.png" align="center" width="300" height="276" /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136780438-3e6fc930-091e-45d6-b1bb-6022cdb0d541.png" align="center" width="300" height="276" /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136780429-a9aecdec-bc62-4504-a056-67bbcf8157d6.png" align="center" width="300" height="276" /></td>
   </tr>   
   <tr align="center">
    <td>(a) Input image</td>
    <td>(b) VARI centers</td>
    <td>(c) GLI centers</td>    
 
  </tr>  
  <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136780437-0ae0b566-1cce-4640-9fd1-801efcf3a4a3.png" align="center" width="300" height="276" /></td>  
    <td><img src= "https://user-images.githubusercontent.com/80779522/136780432-c3a278d1-ef30-453c-8f88-d900b0d5a5e4.png" align="center" width="300" height="276" /></td>
  </tr>
  <tr align="center">
    <td>(c) NGRDI centers</td>    
    <td>(d) NGBDI centers</td>
  </tr>

</table>
  
  **Figure 1** Example of the ```Problematic Areas Detection``` module pipeline a given **RGB input image** and the **points of interest** with blue color based on the extracted VI maps by the ```Vegetation Indices``` module.
  
  
  
     
* **Example of a ```*.json``` file** (2 detected points of interest)
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
