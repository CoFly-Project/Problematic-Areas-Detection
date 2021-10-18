<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Problematic Areas Detection

<!-- This module detects problematic areas of a field and extracts their location based on a given vegetation index of the examined field region. As problematic are considered areas with lowest index values. -->

<!-- The main objective of this module is to detect problematic areas of a field and extract their geolocation based on the extracted vegetation indices of the [```Vegetation Indices```](https://github.com/CoFly-Project/Vegetation-Indices) module. As problematic are considered areas with the lowest index values and they are displayed with red color in VI maps. 
 -->
  
The main objective of the ```Problematic-Areas-Detection``` module is to identify individual field regions of the examined area that present poor conditions, in terms of vegetation  health. Utilizing the indices arrays (```*.npy files```) from [```Vegetation-Indices```](https://github.com/CoFly-Project/Vegetation-Indices) module, a pixel-wise pipeline has been developed to detect the centers of problematic regions. As problematic are considered areas where the corresponding index value is low. Also, this module is able to identify the geolocation of these points of interest based on the RGB image of the examined area and the name of the nearest image captured from the UAV, which is found based on the images' metadata of the UAV mission coverage. 
  
The results of this module are ```*.png``` and  ```*.json``` files (one for each vegetation index). The ```*.png``` files display the detected points of interest on VI maps and the ```*.json``` files contain all the necessary information about:
* the __*geolocation*__  of these points 
* and the __*name of the nearest captured UAV image*__.

  
## How to run
  
1. Clone this repo
2. Open terminal on ~REPO_PATH
3. Run:
```
python3 areas_dection.py --input_image ~IMAGE_PATH --project_path ~PROJECT_PATH --images_dir ~IMAGES_DIR_PATH
```
**ARGUMEΝTS**
  
  * ```~IMAGE_PATH:``` corresponds to the absolute path of the input image of the examined area
  * ```~PROJECT_PATH:``` refers to the absolute path of the folder where the extracted results of the [__Vegetation Indices__](https://github.com/CoFly-Project/Vegetation-Indices) module are saved.
  * ```~IMAGES_DIR_PATH:``` refers to the absolute path of the folder which contains the collected images from the coverage mission of the UAV.

<!-- The ```~IMAGE_PATH``` corresponds to the absolute path of the input image and the ```~PROJECT_PATH``` to the absolute path of the folder where the extracted results of the ```Vegetation Indices''' module are saved. The ```~IMAGES_DIR_PATH``` refers to the absolute path of the folder which contains the collected images from the coverage mission of the UAV. -->
  
> Note: This module is based on the extracted ```*.npy``` files of [```Vegetation Indices```](https://github.com/CoFly-Project/Vegetation-Indices) module. 
  
  
## Results
  
  * **Visualizations**

<!--  ![Problem](https://user-images.githubusercontent.com/80779522/137147004-5f870aaf-d00d-45a7-a213-fe9fc7ced473.png) -->
 
<!--   <table class="center">
   <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136773402-d76cdbea-143c-42e4-9df9-10ec277c902a.png" align="center" width="300" height="276" /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136968887-36be6efd-3523-43c5-871e-9f4cd12a5e0a.png" align="center" width="300" height="276" /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136968861-98640fd0-ba6d-44c2-a644-0d40a36350b1.png" align="center" width="300" height="276" /></td>
   </tr>   
   <tr align="center">
    <td>(a) Input image</td>
    <td>(b) VARI centers</td>
    <td>(c) GLI centers</td>    
 
  </tr>  
  <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136968876-cc0a3be7-634c-4cc1-8120-aba023e6241a.png" align="center" width="300" height="276" /></td>  
    <td><img src= "https://user-images.githubusercontent.com/80779522/136968870-d4fb416d-8f5e-409c-871d-e2f680d8a7ea.png" align="center" width="300" height="276" /></td>
  </tr>
  <tr align="center">
    <td>(c) NGRDI centers</td>    
    <td>(d) NGBDI centers</td>
  </tr>

</table> -->
  
  
<!--   <figure>
  <p align="center">
<img src="https://user-images.githubusercontent.com/80779522/137453916-1c895cb1-10ff-4868-8502-eaebfd77d1e9.png" width="2000" alt="Trulli">
<figcaption align = "center"><p align="center"><b> 
  Figure 2. Example of the Problematic Areas Detection module pipeline with inputs a given RGB input image, the images from the coverage UAV mission and the extracted .npy files from the Vegetation-Indices module and the output are *.png files where the calculated centers of the problematic areas are annotated with blue color with their corresponding *.json files. </b></figcaption>
</figure> -->
    
  
  
     
* **Example of a ```*.json``` file** (2 detected points of interest)
```
  [
    {
        "Lat": 40.573296620493295,
        "Lon": 22.999613709891232,
        "Nearest_image": "129.jpeg"
    },
    {
        "Lat": 40.57339888054105,
        "Lon": 22.998593432140527,
        "Nearest_image": "020.jpeg"
    }
]
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
  * matplotlib
  * scikit-learn
  * gdal

**How to install [GDAL](https://gdal.org)**
* On **Linux**, GDAL binary and Python binding are available through ubuntugis repository. 
  
```sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable```
  
```sudo apt-get install gdal-bin```
  
```sudo apt-get install python3-gdal```
  
  
* On **Windows**, the most easiest way to install GDAL Python Binding is to use the packages build by [Christoph Gohlke](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). The ```*.whl``` package file contains a stand alone GDAL installation including all needed files (binaries, libraries, Python binding, etc.). After downloading the correct version of ```*.whl``` package based on the installed python version on the operating system, install the wheel file with the following command:

```
~PATH_TO_WHL_PACKAGE python.exe -m pip install GDAL-X.X.X-cpXX-cpXXm-win_amd64.whl
```
  
To finalize the installation, it's necessary to define a new Windows environment variables named GDAL_DATA pointing the directory ```C:\Program Files\GDAL\gdal-data``` and PROJ_LIB pointing ```C:\Program Files\GDAL\projlib```.


## Citation
(not published yet)
