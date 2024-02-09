
from .write_coco_json_from_segmentation_path import write_coco_json_from_segmentation_path
from .write_image_annotations_to_folder import write_image_annotations_to_folder
import json, os, shutil 

def write_partition_segmentation_images_to_yolo(
  image_orig_dir_path: str, # Directory containing image .jpgs (i.e., not masks.)
  image_mask_dir_path: str, # Directory containing image mask .pngs. 
  json_write_path: str, # Path to write COCO json to. 
  yolo_folder_path: str, # Folder to write YOLO files into. 
  partition: str, # Subfolder in YOLO folder to write to. "train" | "val" | "test" 
  category_id_map: dict | list, # ID-to-name map 
  limit: int | None=None, # Limit on number of .pngs to go through. If None, does all. 
  verbose: bool=False, *, ask_overwrite=True, print_progress="tqdm", multipolygon_ids=None):
  """ End-to-end writes YOLO file structure from segmentation image (i.e., not segmentation text file) directory. """
  
  if partition not in ["train", "test", "val"]:
    raise Exception(f"partition value '{partition}' not 'train', 'test', or 'val'.")
  
  write_coco_json_from_segmentation_path(
    image_orig_dir_path, 
    image_mask_dir_path, 
    json_write_path, 
    category_id_map, 
    limit, 
    verbose, 
    ask_overwrite=ask_overwrite, 
    print_progress=print_progress, 
    multipolygon_ids=multipolygon_ids
    )
  
  with open(json_write_path, "r") as f:
    coco_dict = json.load(f)
  write_image_annotations_to_folder(os.path.join(yolo_folder_path, "labels", partition), coco_dict)
  if os.path.exists(image_orig_dir_path) and not os.path.exists(os.path.join(yolo_folder_path, "images", partition)):
    shutil.copytree(image_orig_dir_path, os.path.join(yolo_folder_path, "images", partition))
