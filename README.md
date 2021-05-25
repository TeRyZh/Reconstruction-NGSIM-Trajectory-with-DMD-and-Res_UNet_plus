# Reconstructing-NGSIM-Trajectory-with-ResUnet+-and-DMD
This contains the model and data for reconstructing NGSIM dataset

### Table of contents
1. [Scanline and Spatial Temporal Map](#Scanline-and-Spatial-Temporal-Map)
2. [About DMD](#about-Dyanmic-Mode-Decomposition)
3. [Res-Unet+ Model](#Res-Unet+-Model)
4. [NGSIM Data Reconstruction](#NGSIM-Data-Reconstruction)
    * [New I-80 DataSet](#Reconstructed-NGSIM-I-80-Data)
    * [Camera 1](#Camera-1)
    * [Camera 2](#Camera-2)
    * [Camera 3](#Camera-3)
    * [Camera 4](#Camera-4)
5. [Contributing](#contributing) 


### Scanline and Spatial Temporal Map
  The Scanline method stems from the Spatial-Temporal Slice (STS) structure used in computer vision literature. In transportation research, the technique is named as scanline method, which are a set of pixels that can capture object movements on user-selected roadway from the video image. After stacking scanline pixels together over continuous frames, Spatial Temporal Map (STMap) is obtained. On STMap, the horizontal axis shows the time progression, and the vertical axis contains distance information. 
  Two types of scanlines are used in traffic detection, lateral and longitudinal scanlines. The lateral scanline is a cross-section scanline across a lane, whereas the longitudinal scanline is a line along traffic direction. The lateral scanline method was intended primarily for traffic counting and speed measurement. The longitudinal scanline method was used for vehicle tracking and detection. 
  
<img align="middle" width="300" height="200" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/STMap_generation.png" >


### Dyanmic Mode Decomposition

  Dynamic Mode Decomposition is a data-driven analytic method that integrates Fourier transforms and singular value decomposition (SVD). DMD method was first introduced to extract meaningful spatial-temporal coherent structures that dominate dynamic activities in fluid mechanics. DMD method conducts the eigen-decomposition of spatial-temporal coherent structures, therefore can reduce the dimensions of complex systems efficiently without the loss of accuracy. DMD methods have gained traction in many application areas such as fluid dynamics, video processing, control, epidemiology, and financial models. 
The following figure shows the spatial temporal map was separated into foreground and background by decomposing it into low-rank components and sparse components.

<img align="middle" width="600" height="600" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/Mode%20Spectra.png" >

### Res-Unet+ Model

### NGSIM Data Reconstruction

#### Reconstructed NGSIM I-80 Data

#### Camera 1

#### Camera 2

#### Camera 3

#### Camera 4

### contributing
