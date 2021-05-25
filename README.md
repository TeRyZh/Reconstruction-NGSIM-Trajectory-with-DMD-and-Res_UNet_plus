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
<p align="center">
  <img  width="550" height="200" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/STMap_generation.png" >
</p>

### Dyanmic Mode Decomposition

  Dynamic Mode Decomposition is a data-driven analytic method that integrates Fourier transforms and singular value decomposition (SVD). DMD method was first introduced to extract meaningful spatial-temporal coherent structures that dominate dynamic activities in fluid mechanics. DMD method conducts the eigen-decomposition of spatial-temporal coherent structures, therefore can reduce the dimensions of complex systems efficiently without the loss of accuracy. DMD methods have gained traction in many application areas such as fluid dynamics, video processing, control, epidemiology, and financial models. 
The following figure shows the spatial temporal map was separated into foreground and background by decomposing it into low-rank components and sparse components.
<p align="center">
  <img align="middle" width="400" height="400" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/Mode%20Spectra.png" >
</p>

### Res-Unet+ Model
The Res-UNet+ model integrates two common deep learning architectures, using the ResNet block as the backbone and further improves its performance by modifying the UNet model architecture. In the encoding process, the ResNet blocks replace the original encoders in the UNet model. The interconnections between encoding and decoding layers were designed to reduce the semantic gap. To enhance the performance, we added the intra-connections among different levels of decoding stages. Our proposed ResUnet+ model was compared with ResNet, Unet, SegNet, DeepLabv3, FCN and shows best performance. 
<p align="center">
  <img align="middle" width="500" height="400" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/Res-UNet_plus.png" >
   
  <img align="middle" width="300" height="400" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/segmentation_comparison_small.png" >
</p>

### NGSIM Data Reconstruction
One of the most impactful video-based trajectory datasets is the next generation simulation (NGSIM) trajectory dataset [1], which has significantly boosted the traffic flow and modeling research by revealing microscopic traffic characteristics. NGSIM trajectory data, a great asset to traffic flow researcher, has been used to calibrate and evaluate traffic flow models as ground-truth data, demonstrate driving behavior or traffic phenomena, and conduct traffic-state estimation and prediction. However, a growing number of literatures have uncovered the underlying systematic errors in the NGSIM dataset. The first error source is the unstable tracking of vehicles, especially at stop-and-go traffic. The second type of errors in the NGSIM data is caused by the homography projection of raw video that assumes all objects are on the same ground plane. 

The blue lines are plotted with NGSIM data, while the red bars are detected vehicle trajectories by the our method. In the video frame, many of the vehicle trackers are drifted, in contrast, our model output shows very stable tracking capability. The drifting problems frequently happen when cars are joining or leaving a congested platoon. Next figure also displays another tracking error that vehicle 2144 was miss-identified as vehicle 2143 after vehicle 2144 changed from lane 5 to lane 4. This type of error can not be corrected with smoothing or filtering. 

<p align="center">
  <img align="middle" width="500" height="400" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/NGSIM%20Video%20Validation.png" >
</p>

Due to the false assumption of the 2D homography projection that all objects are on the same ground, the NGSIM data only capture the off-ground features of large the vehicles (e.g., trucks and buses) resulting in the self-occlusion issue. The following figure compares the original NGSIM and reconstructed trajectory data in the video frames. For large vehicles, NGSIM data can have significant distance errors (see the large white vehicle from HOV lane in the following Figure). 

<p align="center">
  <img align="middle" width="300" height="200" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/off_ground_feature.png" >
</p>

#### Reconstructed NGSIM I-80 Data

The proposed models were used to identify NGSIM data quality issues and further reconstructed the dataset completely. By processing the NGSIM videos from four cameras (1000 ft area), we conducted a comprehensive cleaning of the datasets and achieved significant quality improvement.

<p align="center">
  <img align="middle" width="900" height="500" src="https://github.com/TeRyZh/Reconstructing-NGSIM-Trajectory-with-ResUnet--and-DMD/blob/main/figs/traj_comparison.png" >
</p>

The reconstructed trajectory data was oganized in original NGSIM format. We provide .fig files for each lane to show the quality improvements using our method to acquire the state-of-the-art trajectory extraction results. 

Trajectory plotted on raw video data can be found in the following link. 

#### [Camera 1](https://www.youtube.com/watch?v=J58d2V2vCGM&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=1)

#### [Camera 2](https://www.youtube.com/watch?v=8mqe8jDigMk&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=2)

#### [Camera 3](https://www.youtube.com/watch?v=jzBmvpLR_ZA&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=3)

#### [Camera 4](https://www.youtube.com/watch?v=L63fW94txoA&list=PLC4d9Yu1vCsn4mAESXLUDmyxFC0vR3KOI&index=4)

### Contributing
If you found any errors or bugs in our program or new dataset please contact: terry.tianya.zhang@gmail.com
