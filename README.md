
Converts segmentation *images* => COCO JSON => YOLO segmentation format. (And, parses category list from file.) 

| Function | Description | 
| --- | --- | 
| `get_category_list_from_file` | Parse list of category names from file. | 
| `write_coco_json_from_segmentation_path` | Converts segmentation image masks to segmentation lists, storing them in COCO JSON format. 
| `write_image_annotations_to_folder` | COCO JSON => YOLO segmentation format. 

Each has a **doc string** and **examples**. (See `main()` or `__main__` for examples.)

**Why?** 
- Some datasets save the labels as images themselves. YOLO needs them as a list of points, not as an image. 
- `write_coco_json_from_segmentation_path` is an adapted version of an existing online script that converts from label images to COCO JSON format. 
- From there, `write_image_annotations_to_folder` converts from COCO to YOLO. 
