# SemanticKITTI ros Publisher

ROS publisher node for SemanticKITTI dataset  
video: https://youtu.be/eKNi2yuQOxc

## Dependencies
rospy  
numpy


## Usage

(1) download SemanticKITTI dataset  
http://semantic-kitti.org/index.html


(2) type the following command  

python main.py -d (dataset_path) -s (sequence_id)  
```sh
ex) python main.py -d /home/dongwonshin/Desktop/dataset/KITTI_odometry/dataset/sequences -s 00
```