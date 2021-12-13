<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Problematic Areas Detection
  
The main objective of the ```Problematic-Areas-Detection``` module is to identify individual field regions of the examined area that present poor conditions, in terms of vegetation  health. Utilizing the indices arrays (```*.npy files```) extracted from the [```Vegetation-Indices```](https://github.com/CoFly-Project/Vegetation-Indices) module, a pixel-wise pipeline has been developed to detect the problematic regions. As problematic are considered areas where the corresponding index value is low. For every detected area, the  center of mass is calculated leading to a set of points, considered as points of interest. 


Τhe module takes as inputs the extracted *VI array (npy file)*, and the corresponding *VI image representation (tif file)* as extracted from the [```Vegetation-Indices```](https://github.com/CoFly-Project/Vegetation-Indices/tree/main). The output of the module is an image representation of the VI where the detected points of interest are annotated accordingly and a json file containing for each detected point the __``` geolocation```__ or __```pixel coordinates```__ of the point of interest. The extracted files are named according to the corresponding name of VI, e.g. VARI.json. In Figure 1, we present an overview of the Problematic-Areas-Detection module.
  
  
<!-- * the __*filename*__ of the image captured closest to it -->
  
<!-- https://user-images.githubusercontent.com/80779522/145570181-047eb5d2-ae6a-482d-84f5-3a0040dd87d8.png -->
<!-- https://user-images.githubusercontent.com/80779522/138094954-cffa6169-e677-4c67-8a54-2ed4a9bfa387.png --> 

  https://user-images.githubusercontent.com/80779522/145800146-1def5712-dbfa-4a91-96b2-cf709c0d965f.png
  <p align="center">
<img src="https://user-images.githubusercontent.com/80779522/145800146-1def5712-dbfa-4a91-96b2-cf709c0d965f.png"/>
<figcaption align = "center"><p align="center">
  Figure 1. Workflow of the Problematic-Areas-Detection module. The points of interest are displayed with blue color.</figcaption>
</figure>  
  <!-- <p align="center">
<img src="https://user-images.githubusercontent.com/80779522/144032915-41b0588b-a86f-40ff-a4c6-5942505a15f9.png"/>
<figcaption align = "center"><p align="center">
  Figure 1. Workflow of the Problematic-Areas-Detection module. The points of interest are displayed with blue color.</figcaption>
</figure> -->
  



## How to run
  
1. Clone this repo
2. Open terminal on ~REPO_PATH
3. Run:
```
python3 areas_dection.py --input_image ~IMAGE_PATH --index ~VI_ARRAY_PATH
```
**ARGUMEΝTS**
  * ```--input_image```  refers to the path of the input VI image representation of the examined area
  * ```--index``` refers to the path where the correspndinding VI array is stored
  
## Results
  
### Visualizations

  <table >
   <tr align="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/137704570-c2febf14-7cae-437b-ae1b-6ffd44130445.png" align="center" width="210" height="180"/></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/137921109-bbd040d6-6a16-4d09-9e12-a7dc8d265dc5.png" align="center" width="210" height="180"/></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/137704566-7bde622c-1137-4841-9276-370c65ee663b.png" align="center" width="210" height="180"/></td>  
    <td><img src= "https://user-images.githubusercontent.com/80779522/137704559-f291824f-0d96-4568-acc8-46857197f6b6.png" align="center" width="210" height="180"/></td>
   </tr>   
   <tr align="center">
    <td>(a) VARI</td>
    <td>(b) GLI</td>   
    <td>(c) NGRDI</td>    
    <td>(d) NGBDI</td>
     </table>
     <figcaption align = "center"><p align="center">
  Figure 2. Detected points of interest (blue marks) for a set of different VIs.
    </figcaption>
  
     
### Example of a ```*.json``` file (2 detected points of interest)

Presuming that VI image representation is georeferenced, the _*.json_ file has the following format:
    
```
[
    {
        "Lat": 40.573296620493295,
        "Lon": 22.999613709891232
    },
    {
        "Lat": 40.57339888054105,
        "Lon": 22.998593432140527
    }
]
```

Otherwise:

```
[
    {
        "X_pixel": 1040,
        "Y_pixel": 1022
    },
    {
        "X_pixel": 2155,
        "Y_pixel": 890
    }
]
```

## Dependencies 
Install all the neccecary dependencies using ```pip3 install <package name>```

Required packages:
* opencv-python (version >= 4.5.3)
* numpy (version >= 1.21.3)
* scipy (version >= 1.4.1)
* gdal (version >= 3.2.2)
* argparse (version >= 1.1)
* skimage (version >= 0.18.1)
* matplotlib (version >= 3.2.2)
* scikit-learn (version >= 0.24.0)
* json (version >= 2.0.9)
* exif (version >= 1.3.1)

<!-- <div align="center">
  
|Package|Vesrion|
| :---: | :---: |
opencv-python | 4.5.3
numpy | 1.21.3
scipy | 1.4.1
gdal | 3.2.2
argparse | 1.1
skimage | 0.18.1
matplotlib | 3.2.2
scikit-learn | 0.24.0
json | 2.0.9
exif | 1.3.1
  
</div>
<figcaption align = "center"><p align="center">Table 1. Required packages and their versions, respectively.</figcaption>
</figure> -->
  

**How to install [GDAL](https://gdal.org)**
* On **Linux**, GDAL binary and Python binding are available through ubuntugis repository. 
  
```
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get install gdal-bin
sudo apt-get install python3-gdal
```
  
  
* On **Windows**, the easiest way to install GDAL Python Binding is to use the packages build by [Christoph Gohlke](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). The ```*.whl``` package file contains a stand alone GDAL installation including all needed files (binaries, libraries, Python binding, etc.). After downloading the correct version of ```*.whl``` package based on the installed python version on the operating system, install the wheel file with the following command:

```
~PATH_TO_WHL_PACKAGE python.exe -m pip install GDAL-X.X.X-cpXX-cpXXm-win_amd64.whl
```
  
To finalize the installation, it's necessary to define new Windows environment variables:
* **GDAL_DATA** pointing the directory ```C:\Program Files\GDAL\gdal-data```
* **GDAL_DRIVER_PATH** pointing the directory ```C:\Program Files\GDAL\gdalplugins```
* and **PROJ_LIB** pointing ```C:\Program Files\GDAL\projlib```


## Citation
(not published yet)

## Acknowledgment
This research has been financed by the European Regional Development Fund of the European Union and Greek national funds through the Operational Program Competitiveness, Entrepreneurship and Innovation, under the call RESEARCH - CREATE - INNOVATE (T1EDK-00636).
