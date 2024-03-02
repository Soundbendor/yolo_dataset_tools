
"""
write_coco_json_from_segmentation_path creates a JSON with the following format: 

"images": [
    {
      "file_name": "00004421.jpg",
      "height": 384,
      "width": 512,
      "id": 0
    },
    {
      "file_name": "00006089.jpg",
      "height": 256,
      "width": 256,
      "id": 1
    },
    {
      "file_name": "00004821.jpg",
      "height": 396,
      "width": 512,
      "id": 2
    },

 "annotations": [
    {
      "segmentation": [
        [
          15.0,
          176.5,
          8.0,
          170.5,
          -0.5,
          172.0,
          -0.5,
          0.0,
          137.0,
          -0.5,
          135.0,
          1.5,
          110.0,
          11.5,
          104.0,
          17.5,
          97.0,
          19.5,
          76.0,
          20.5,
          58.0,
          24.5,
          47.0,
          28.5,
          40.5,
          36.0,
          38.5,
          44.0,
          32.5,
          56.0,
          31.5,
          85.0,
          37.5,
          111.0,
          45.5,
          124.0,
          44.5,
          141.0,
          40.5,
          149.0,
          32.0,
          152.5,
          31.5,
          156.0,
          22.0,
          163.5,
          17.0,
          157.5,
          15.5,
          158.0,
          18.5,
          169.0,
          15.0,
          176.5
        ]
      ],
      "area": 8075.0,
      "iscrowd": 0,
      "image_id": 0,
      "bbox": [
        -0.5,
        -0.5,
        137.5,
        177.0
      ],
      "category_id": 0,
      "id": 0
    },
    {
      "segmentation": [
        [
          511.0,
          94.5,
          504.0,
          87.5,
          471.0,
          69.5,
          411.0,
          49.5,
          397.0,
          46.5,
          374.0,
          32.5,
          326.0,
          20.5,
          295.0,
          23.5,
          279.0,
          14.5,
          236.0,
          6.5,
          215.5,
          0.0,
          511.0,
          -0.5,
          511.0,
          94.5
        ]
      ],
      "area": 11228.0,
      "iscrowd": 0,
      "image_id": 0,
      "bbox": [
        215.5,
        -0.5,
        295.5,
        95.0
      ],
      "category_id": 0,
      "id": 1
    },


write_image_annotations_to_folder converts above dictionary to YOLO's segmentation format: 
image_number.txt: 
category_id PROP_HEIGHT1 PROP_WIDTH1 ... 
"""

"""
Take "id" => "file_name" from "images" key in JSON. 
Take "image_id" from each list of dictionaries in "annotations" key in JSON. 
"""

from bidict import bidict 
from collections import defaultdict 
import os 

def write_image_annotations_to_folder(folder_path, coco_dict, *, ask_overwrite=True):
  if ask_overwrite:
    _get_confirmation_from_user_about_overwrite(folder_path)
  image_id_to_file_name_map = get_image_id_to_file_name_map(coco_dict)
  image_id_to_height_width_map = get_image_id_to_height_width_map(coco_dict)
  annotations = coco_dict["annotations"]
  normalize_segmentation_coords(annotations, image_id_to_height_width_map)
  image_id_to_annotation_list = get_image_id_to_list_of_annotations(annotations)
  # print(image_id_to_annotation_list)
  for image_id, annotation_list in image_id_to_annotation_list.items():
    _write_image_annotation_to_file(folder_path, image_id_to_file_name_map[image_id], annotation_list)

def main():
  import os, json 
  JSON_PATH = "/home/joey/yolo_dataset_tools/test_json_write_path.json"
  with open(JSON_PATH, "r") as f:
    coco_dict = json.load(f)
  FOLDER_PATH = "test_folder_write/"
  write_image_annotations_to_folder(FOLDER_PATH, coco_dict)

def get_image_id_to_file_name_map(coco_json) -> dict:
  """ Returns {"image_id" => "file_name", ...}. """
  dct = bidict()
  for image_dict in coco_json["images"]:
    dct[image_dict["id"]] = image_dict["file_name"]
    
  return dct 

def get_image_id_to_height_width_map(coco_json) -> dict:
  """ Returns {"image_id" => {"height": ..., "width": ...}. """
  dct = {}
  for image_dict in coco_json["images"]:
    dct[image_dict["id"]] = {"height": image_dict["height"], "width": image_dict["width"]}
  return dct

def normalize_segmentation_coords(annotations, image_id_to_height_width_map):
  """ 
  Divides absolute coords by height and width. 
  COCO uses absolute coords, while YOLO uses proportions. 
  NOTE: Mutates annotations in place. Does not return anything. 
  """
  def normalize_segment(segment, width, height) -> list:
    normalized = []
    for i in range(0, len(segment), 2):
      normalized.append(segment[i] / width)
      normalized.append(segment[i+1] / height)
    return normalized
  
  for annotation in annotations:
    # print("annotation:", annotation)
    seg = annotation["segmentation"][0] # For some reason nested list. 
    height_width = image_id_to_height_width_map[annotation["image_id"]]
    width = height_width["width"]
    height = height_width["height"]
    annotation["segmentation"] = normalize_segment(seg, width, height)

def get_image_id_to_list_of_annotations(annotations) -> dict:
  """ { "image_id" => [ {"segmentation": [...], "category_id": ...}, { ... }, ...] }. """
  dct = defaultdict(list)
  for annotation in annotations:
    image_id = annotation["image_id"]
    seg      = annotation["segmentation"]
    cat_id   = annotation["category_id"]
    dct[image_id].append({"segmentation": seg, "category_id": cat_id})
  return dct 

def _format_category_and_segmentation(cat_id, seg_list):
  return f"{cat_id} {' '.join([str(x) for x in seg_list])}"

def _write_image_annotation_to_file(folder_path, image_name, annotation_list):
  """ Writes annotation text file for single image, given folder_path, image_name, and annotation_list. """
  # For single image. 
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  with open(f"{folder_path}/{image_name.split('.')[0]}.txt", "w") as f:
    for annotation in annotation_list:
      cat_id = annotation["category_id"]
      seg_list = annotation["segmentation"]
      f.write(_format_category_and_segmentation(cat_id, seg_list) + "\n")
      
def _get_confirmation_from_user_about_overwrite(folder_path):
  """ Returns if user wants to overwrite. Otherwise, raises SystemExit. """
  if os.path.exists(folder_path):
    while True:
      inp = input(f"\033[91m{folder_path} already exists. Overwrite existing annotation files with duplicate names (will not overwrite folder)? (y/n)\033[0m ")
      if inp.lower() in ["n", "no"]:
        print("Raising SystemExit.")
        raise SystemExit()
      elif inp.lower() in ["y", "yes"]:
        print("Writing into same folder.")
        return 
      else:
        print("Invalid input. Please enter y/n.")

if __name__ == "__main__":
  main()
