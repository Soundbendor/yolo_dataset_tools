
### Install 
**From URL**:
`python -m pip install -U git+https://github.com/Soundbendor/yolo_dataset_tools.git#egg=yolo_dataset_tools`

**From local clone**:
`python -m pip install -U PATH_TO_YOLO_DATASET_TOOLS`

### Interface files 
`dataset_merger.pyi`
`dataset.pyi`
`image.pyi`
`annotation.pyi`

### Functions 
1. Converts segmentation *images* => COCO JSON => YOLO segmentation format. (And, parses category list from file.) 
2. Merges YOLO segmentation datasets by writing to new folder + storing metadata as JSON. 

| Function/class | Description | 
| --- | --- | 
| `get_category_list_from_file` | Parse list of category names from file. | 
| `write_partition_segmentation_images_to_yolo` | Combines `write_coco_json_from_segmentation_path`, `write_image_annotations_to_folder`, and creation of partition folder. |
| `write_coco_json_from_segmentation_path` | Converts segmentation image masks to segmentation lists, storing them in COCO JSON format. 
| `write_image_annotations_to_folder` | COCO JSON => YOLO segmentation format. 
| `DatasetMerger` | Merge datasets. 
| `Dataset` | Access dataset items. 

Each has a **doc string** and **examples**. (See `main()` or `__main__` for examples.)

### Purpose 
- Some datasets save the labels as images themselves. YOLO needs them as a list of points, not as an image. 
- `write_coco_json_from_segmentation_path` is an adapted version of an existing online script that converts from label images to COCO JSON format. 
- From there, `write_image_annotations_to_folder` converts from COCO to YOLO. 
