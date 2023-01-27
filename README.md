# Reconstruction-NGSIM-Trajectory-with-DMD-and-Res_UNet_plus
This repo contains the model and data for reconstructing NGSIM dataset. [Paper Link](https://arxiv.org/abs/2201.04755)

### Table of contents
1. [Scanline and Spatial Temporal Map](#Scanline-and-Spatial-Temporal-Map)
2. [About DMD](#Dyanmic-Mode-Decomposition)
3. [Res-Unet+ Model](#Res_UNet_plus-Model)
4. [NGSIM Data Reconstruction](#NGSIM-Data-Reconstruction)
    * [New I-80 DataSet](#New-NGSIM-I-80-Data)
    * [Camera 1](#Camera-1)
    * [Camera 2](#Camera-2)
    * [Camera 3](#Camera-3)
    * [Camera 4](#Camera-4)
5. [Contributing](#contributing) 

### Scanline-and-Spatial-Temporal-Map
  The Longitudinal Scanline method stems from the Spatial-Temporal Slice (STS) structure used in computer vision literature. In transportation research, the technique is named as scanline method, which are a set of pixels that can capture object movements on user-selected roadway from the video image. After stacking scanline pixels together over continuous frames, Spatial Temporal Map (STMap) is obtained. On STMap, the horizontal axis shows the time progression, and the vertical axis contains distance information. 

<p align="center">
  <img  width="550" height="200" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/STMap_generation.png" >
</p>

### Dyanmic-Mode-Decomposition

  Dynamic Mode Decomposition is a data-driven analytic method that integrates Fourier transforms and singular value decomposition (SVD). DMD method was first introduced to extract meaningful spatial-temporal coherent structures that dominate dynamic activities in fluid mechanics. DMD method conducts the eigen-decomposition of spatial-temporal coherent structures, therefore can reduce the dimensions of complex systems efficiently without the loss of accuracy. DMD methods have gained traction in many application areas such as fluid dynamics, video processing, control, epidemiology, and financial models. 
The following figure shows the spatial temporal map was separated into foreground and background by decomposing it into low-rank components and sparse components.
<p align="center">
  <img align="middle" width="400" height="400" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/Mode%20Spectra.png" >
</p>

### Res_UNet_plus-Model
The Res-UNet+ model integrates two common deep learning architectures, using the ResNet block as the backbone and further improves its performance by modifying the UNet model architecture. In the encoding process, the ResNet blocks replace the original encoders in the UNet model. The interconnections between encoding and decoding layers were designed to reduce the semantic gap. To enhance the performance, we added the intra-connections among different levels of decoding stages. Our proposed ResUnet+ model was compared with ResNet, Unet, SegNet, DeepLabv3, FCN and shows best performance. 
<p align="center">
   <img align="middle" width="600" height="400" src="https://github.com/TeRyZh/Reconstruction-NGSIM-Trajectory-with-DMD-and-Res_UNet_plus/blob/main/figs/Model%20Performance.png" >
</p>

### NGSIM-Data-Reconstruction
A growing number of literatures have uncovered the underlying systematic errors in the NGSIM dataset. The first error source is the unstable tracking of vehicles, especially at stop-and-go traffic. The second type of errors in the NGSIM data is caused by the homography projection of raw video that assumes all objects are on the same ground plane. 

The blue lines are plotted with NGSIM data, while the red bars are detected vehicle trajectories by the our method. In the video frame, many of the vehicle trackers are drifted, in contrast, our model output shows very stable tracking capability. The drifting problems frequently happen when cars are joining or leaving a congested platoon. The lower half figure also displays another tracking error that vehicle 2144 was miss-identified as vehicle 2143 after vehicle 2144 changed from lane 5 to lane 4. 

<p align="center">
   <img align="middle" width="600" height="400" src="https://github.com/TeRyZh/Reconstruction-NGSIM-Trajectory-with-DMD-and-Res_UNet_plus/blob/main/figs/NGSIM%20Video%20Validation.png" >
</p>


### New-NGSIM-I-80-Data

<p align="center">
   <img align="middle" width="900" height="500" src="https://github.com/TeRyZh/Reconstruction-NGSIM-Trajectory-with-DMD-and-Res_UNet_plus/blob/main/figs/traj_comparison.png" >
</p>

#### [Camera-1](https://www.youtube.com/watch?v=J58d2V2vCGM&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=1)

#### [Camera-2](https://www.youtube.com/watch?v=8mqe8jDigMk&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=2)

#### [Camera-3](https://www.youtube.com/watch?v=jzBmvpLR_ZA&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=3)

#### [Camera-4](https://www.youtube.com/watch?v=L63fW94txoA&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=4)

### Contributing
If you found any errors or bugs in our program or new dataset please contact: terry.tianya.zhang@gmail.com
