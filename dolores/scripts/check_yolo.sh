# List the contents of the current directory
!ls

# Calculate anchors for your custom dataset
!./darknet detector calc_anchors data/obj.data -num_of_clusters 9 -width 800 -height 800 -show

# Modify YOLOv3-SPP configuration file (yolov3-spp.cfg) using sed commands

# Set batch size to 64
!sed -i 's/batch=1/batch=64/g' cfg/yolov3-spp.cfg

# Set subdivisions to 32
!sed -i 's/subdivisions=1/subdivisions=32/g' cfg/yolov3-spp.cfg

# Adjust input width and height to 800x800
!sed -i 's/width=608/width=800/g' cfg/yolov3-spp.cfg
!sed -i 's/height=608/height=800/g' cfg/yolov3-spp.cfg

# Set max_batches to 116000
!sed -i 's/max_batches = 500200/max_batches = 116000/g' cfg/yolov3-spp.cfg

# Adjust training steps
!sed -i 's/steps=400000,450000/steps=92800,104400/g' cfg/yolov3-spp.cfg

# Set the number of classes to 58
!sed -i 's/classes=80/classes=58/g' cfg/yolov3-spp.cfg

# Adjust the number of filters to 189
!sed -i 's/filters=255/filters=189/g' cfg/yolov3-spp.cfg

# Display the modified configuration file
!cat cfg/yolov3-spp.cfg