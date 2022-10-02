# NASAHackathon2022

## You are welcome to click the link below to view our project demo.

[Project Demo Link](http://nasa.thebestyea.net/)


##UAV ROAD INSPECTION MODULE
###Requirements for Windows, Linux and macOS

* CMake >= 3.18: https://cmake.org/download/
*  Powershell (already installed on windows): https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell
* CUDA >= 10.2: https://developer.nvidia.com/cuda-toolkit-archive (on Linux do Post-installation Actions)
* OpenCV >= 2.4: use your preferred package manager (brew, apt), build from source using vcpkg or download from OpenCV official site (on Windows set system variable * OpenCV_DIR = C:\opencv\build - where are the include and x64 folders image)
* cuDNN >= 8.0.2 https://developer.nvidia.com/rdp/cudnn-archive (on Linux copy cudnn.h,libcudnn.so... as described here https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html#installlinux-tar , on Windows copy cudnn.h,cudnn64_7.dll, cudnn64_7.lib as described here https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html#installwindows )
* GPU with CC >= 3.0: https://en.wikipedia.org/wiki/CUDA#GPUs_supported

### Train model
#### Step 1. Download  Darknet UAVRoadInspectionModule/darknet
#### Step 2. Revise GPU, CUDNN, CUDNN_HALF, OPENCV in Makefile to 1
    sed -i "s/GPU=0/GPU=1/g" darknet/Makefile
    sed -i "s/CUDNN=0/CUDNN=1/g" darknet/Makefile
    sed -i "s/CUDNN_HALF=0/CUDNN_HALF=1/g" darknet/Makefile
    sed -i "s/OPENCV=0/OPENCV=1/g" darknet/Makefile

#### Step 3. Compile
    cd darknet; 
    make
#### Step 4. Create a folder to put files
* 4-1 Create a folder named Road_detection

      cd ..; mkdir Road_detection
      cd Road_detection
* 4-2 Create two folders for cfg and weights, and copy road.data, road.names in cfg
      
      import os
      import shutil
      
      if not os.path.exists(“Road_detection”):
        os.mkdir(“Road_detection”)
      if not os.path.exists(“Road_detection/cfg”):
        os.mkdir(“Road_detection/cfg”) 
        os.mkdir(“Road_detection/weights”)
      if not os.path.exists(“Road_detection/cfg/road.data”):
        shutil.copyfile(“darknet/cfg/coco.data”, “Road_detection/cfg/road.data”)
      if not os.path.exists(“Road_detection/cfg/road.names”):
        shutil.copyfile(“darknet/cfg/coco.names”, “Road_detection/cfg/road.names”)
#### Step 5. Prepare a training data set

File path:

* darknet
* Road_detection
    - cfg
        * road.data
        * road.names
        *	train.txt	//the path of training data
        *	valid.txt	//the path of valida data
    -	weights
    -	road_train	//contain images and label datas
    -	road_valid	//contain images and label datas

#### Step 6. Revise road.data and road.names

road.data
Change the number of class and the path
road.names
Write classes

#### Step 7. Revise yolov4-tiny.cfg

Copy yolov4-tiny-custom.cfg to detection file from darknet/cfg/, and rename yolov4-tiny-obj.cfg

    cp ../darknet/cfg/yolov4-tiny-custom.cfg cfg/yolov4-tiny-obj.cfg
    # Check parameters
    sed -n -e 8p -e 9p -e 212p -e 220p -e 263p -e 269p cfg/yolov4-tiny-obj.cfg
    # Show as follows
    width=416
    height=416
    filters=255
    classes=80
    filters=255
    classes=80
    # Revise the parameters, filters=(classes+5)*3
    sed -i '212s/255/filters/' cfg/yolov4-tiny-obj.cfg
    sed -i '220s/80/classes/' cfg/yolov4-tiny-obj.cfg
    sed -i '263s/255/filters/' cfg/yolov4-tiny-obj.cfg
    sed -i '269s/80/classes/' cfg/yolov4-tiny-obj.cfg
    # Check parameters again
    sed -n -e 212p -e 220p -e 263p -e 269p cfg/yolov4-tiny-obj.cfg


#### Step 8. Revise the value of anchors

    cd ../darknet
    ./darknet detector calc_anchors ../Face_detection/cfg/face.data -num_of_clusters 6 -width 416 -height 416 -showpause
    
#### Step 9. Download yolov4.conv.137 to Road_detection/cfg

    https://drive.google.com/open?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp
    
#### Step 10. Start training

    ./darknet detector train ./Road_detection/cfg/road.data ./Road_detection/cfg/yolov4-tiny-obj.cfg ./Road_detection/cfg/yolov4.conv.137 -dont_show

### Start road inspection

#### Step 1. Rename the video taken by UAV
    rename gopro=1.mp4 argus=2.mp4

#### Step 2. Convert the video format to avi
    ffmpeg -i 1.mp4 -vocodec copy -acode copy 1.avi
#### Step 3. Split the video. (1 picture/2sec), and revise start_index in video_process.py(ReportGenerationSystem/video_process.py)
    python3 video_process.py
#### Step 4. Combine the information of sensor datas, and rename 1.txt

#### Step 5. Run yolo

    ./darknet detector test UAVRoadInspectionModule/bridge/cfg/bridge.data UAVRoadInspectionModule/bridge/cfg/yolov4-tiny-obj.cfg       
    UAVRoadInspectionModule/bridge/cfg/weights/yolov4-tiny-obj_final.weights
    UAVRoadInspectionModule/bridge/bridge/output.txt
    
#### Step 6. Copy the file of result to the file “ReportGenerationSystem/pdfgen”

#### Step 7. Generate a report of road inspection

    python3 pdfgen.py
