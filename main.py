import rospy
import struct

from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

import numpy as np
import argparse

def make_semantic_points(dataset_path, seq_id, cnt):
    my_label_file = '%s/%s/labels/%06d.label' % (dataset_path, seq_id, cnt)
    my_point_file = '%s/%s/velodyne/%06d.bin' % (dataset_path, seq_id, cnt)
    
    f = open(my_label_file, "r")
    labels = np.fromfile(f, dtype=np.uint16)
    f.close()
    labels = labels.reshape(-1,2)
    
    f = open(my_point_file, "r")
    points = np.fromfile(f, dtype=np.float32)
    f.close()
    points = points.reshape(-1,4)
    
    # points[:,3] = labels[:,0] # for instance label
    points[:,3] = labels[:,1] # for semantic label

    fields = [PointField('x', 0, PointField.FLOAT32, 1),
            PointField('y', 4, PointField.FLOAT32, 1),
            PointField('z', 8, PointField.FLOAT32, 1),
            PointField('intensity', 12, PointField.UINT32, 1),
            ]

    return points, fields

if __name__ == "__main__":

    parser = argparse.ArgumentParser("./main.py")
    parser.add_argument(
        '--dataset_path', '-d',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--seq_id', '-s',
        type=str,
        required=True,
    )
    FLAGS, unparsed = parser.parse_known_args()

    rospy.init_node("SemanticKITTI_ros_publisher")
    pub = rospy.Publisher("point_cloud2", PointCloud2, queue_size=2)
    cnt = 0

    while not rospy.is_shutdown():
        header = Header()
        header.frame_id = "map"
        points, fields = make_semantic_points(FLAGS.dataset_path,FLAGS.seq_id,cnt)
        cnt += 1
        pc2 = point_cloud2.create_cloud(header, fields, points)

        pc2.header.stamp = rospy.Time.now()
        pub.publish(pc2)
        # rospy.sleep(0.1)