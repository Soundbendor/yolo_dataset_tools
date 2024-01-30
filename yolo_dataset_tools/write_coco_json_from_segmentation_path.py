
from bidict import bidict 
from .get_category_list_from_file import get_category_list_from_file 
from pprint import pprint 
from tqdm import tqdm 

def write_coco_json_from_segmentation_path(image_orig_dir_path: str, image_mask_dir_path: str, json_write_path: str, category_id_map: dict | list, limit: int | None=None):
  """
  image_orig_dir_path : Path to directory of original images. 
  image_mask_dir_path : Path to directory of segmentation mask images. 
  json_write_path     : Path to write JSON to. 
  category_id_map     : { "category_name_0" : category_id0, ... }. If list provided, enumerates + inverts to get dictionary. 
  limit               : How many images to convert + write. If None, does all. 
  """
  
  _get_confirmation_from_user_about_overwrite(json_write_path)
  
  # If category ID is list, then enumerate and return map from name to ID. 
  if isinstance(category_id_map, list):
    category_id_map = bidict({ category_name : i for i, category_name in enumerate(category_id_map) })
    
  # Get the colors for the category names. 
  category_colors = { _id_to_color_str(category_id): category_id for (category_name, category_id) in category_id_map.items() }

  # Getting empty COCO json. 
  coco_format = get_coco_json_format()

  coco_format["categories"] = create_category_annotation(category_id_map)
  
  coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(image_mask_dir_path, category_colors, limit=limit)
  
  pprint(f"json dumps: {json.dumps(coco_format)}", indent=2)
  
  with open(json_write_path, "w") as outfile:
    json.dump(coco_format, outfile, indent=2)

def _id_to_color_str(id: int) -> str:
  return f"({id}, {id}, {id})"

def main():
  FOOD_SEG_103_TEST_ORIG_IMAGES_PATH  = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/Test/images/"
  FOOD_SEG_103_TEST_LABEL_IMAGES_PATH = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/Test/labels_images/"
  FOOD_SEG_103_JSON_WRITE_PATH        = "test_json_write_path.json"
  FOOD_SEG_103_CATEGORY_ID_MAP        = get_category_list_from_file("/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/category_id.txt", start_line=0)
  LIMIT                               = 32 
  write_coco_json_from_segmentation_path(
    FOOD_SEG_103_TEST_ORIG_IMAGES_PATH,
    FOOD_SEG_103_TEST_LABEL_IMAGES_PATH,
    FOOD_SEG_103_JSON_WRITE_PATH,
    FOOD_SEG_103_CATEGORY_ID_MAP,
    LIMIT,
  )

def _get_confirmation_from_user_about_overwrite(json_write_path):
  """ Returns if user wants to overwrite. Otherwise, raises SystemExit. """
  if os.path.exists(json_write_path):
      while True:
          inp = input(f"\033[91m{json_write_path} already exists. Overwrite? (y/n)\033[0m ")
          if inp.lower() in ["n", "no"]:
              print("Raising SystemExit.")
              raise SystemExit()
          elif inp.lower() in ["y", "yes"]:
              print("Overwriting.")
              return 
          else:
              print("Invalid input. Please enter y/n.")

# SOURCE: https://github.com/chrise96/image-to-coco-json-converter/blob/master/create-custom-coco-dataset.ipynb 

# # # START OF src/create_annotations.py IN ORIGINAL REPO. 

from PIL import Image                                      # (pip install Pillow)
import numpy as np                                         # (pip install numpy)
from skimage import measure                                # (pip install scikit-image)
from shapely.geometry import Polygon, MultiPolygon         # (pip install Shapely)
import os
import json

def create_sub_masks(mask_image, width, height):
    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = mask_image.getpixel((x,y))[:3]

            # Check to see if we have created a sub-mask...
            pixel_str = str(pixel)
            sub_mask = sub_masks.get(pixel_str)
            if sub_mask is None:
               # Create a sub-mask (one bit per pixel) and add to the dictionary
                # Note: we add 1 pixel of padding in each direction
                # because the contours module doesn"t handle cases
                # where pixels bleed to the edge of the image
                sub_masks[pixel_str] = Image.new("1", (width+2, height+2))

            # Set the pixel value to 1 (default is 0), accounting for padding
            sub_masks[pixel_str].putpixel((x+1, y+1), 1)

    return sub_masks

def create_sub_mask_annotation(sub_mask):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    contours = measure.find_contours(np.array(sub_mask), 0.5, positive_orientation="low")

    polygons = []
    segmentations = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)
        
        if(poly.is_empty):
            # Go to next iteration, dont save empty values in list
            continue

        polygons.append(poly)

        segmentation = np.array(poly.exterior.coords).ravel().tolist()
        segmentations.append(segmentation)
    
    return polygons, segmentations

def create_category_annotation(category_dict):
    category_list = []

    for key, value in category_dict.items():
        category = {
            "supercategory": key,
            "id": value,
            "name": key
        }
        category_list.append(category)

    return category_list

def create_image_annotation(file_name, width, height, image_id):
    images = {
        "file_name": file_name,
        "height": height,
        "width": width,
        "id": image_id
    }

    return images

def create_annotation_format(polygon, segmentation, image_id, category_id, annotation_id):
    min_x, min_y, max_x, max_y = polygon.bounds
    width = max_x - min_x
    height = max_y - min_y
    bbox = (min_x, min_y, width, height)
    area = polygon.area

    annotation = {
        "segmentation": segmentation,
        "area": area,
        "iscrowd": 0,
        "image_id": image_id,
        "bbox": bbox,
        "category_id": category_id,
        "id": annotation_id
    }

    return annotation

def get_coco_json_format():
    # Standard COCO format 
    coco_format = {
        "info": {},
        "licenses": [],
        "images": [{}],
        "categories": [{}],
        "annotations": [{}]
    }

    return coco_format
  
# # # END OF SRC.ANNOTATIONS IN ORIGINAL REPO. 

# # # START OF create-custom-coco-dateset.ipynb IN ORIGINAL REPO. 

import glob

# Label ids of the dataset
# category_ids = {
#     "outlier": 0,
#     "window": 1,
#     "wall": 2,
#     "balcony": 3,
#     "door": 4,
#     "roof": 5,
#     "sky": 6,
#     "shop": 7,
#     "chimney": 8
# }

# Define which colors match which categories in the images
# category_colors = {
#     "(0, 0, 0)": 0, # Outlier
#     "(255, 0, 0)": 1, # Window
#     "(255, 255, 0)": 2, # Wall
#     "(128, 0, 255)": 3, # Balcony
#     "(255, 128, 0)": 4, # Door
#     "(0, 0, 255)": 5, # Roof
#     "(128, 255, 255)": 6, # Sky
#     "(0, 255, 0)": 7, # Shop
#     "(128, 128, 128)": 8 # Chimney
# }

# Define the ids that are a multiplolygon. In our case: wall, roof and sky
multipolygon_ids = [2, 5, 6]

# Get "images" and "annotations" info 
def images_annotations_info(maskpath, category_colors, limit=None):
    # This id will be automatically increased as we go
    annotation_id = 0
    image_id = 0
    annotations = []
    images = []
    
    files_to_iter = glob.glob(maskpath + "*.png")
    if limit is not None:
      files_to_iter = files_to_iter[:limit]
    
    for mask_image in tqdm(files_to_iter, desc=f"Creating annotations for {maskpath}."):
        # The mask image is *.png but the original image is *.jpg.
        # We make a reference to the original file in the COCO JSON file
        original_file_name = os.path.basename(mask_image).split(".")[0] + ".jpg"

        # Open the image and (to be sure) we convert it to RGB
        mask_image_open = Image.open(mask_image).convert("RGB")
        w, h = mask_image_open.size
        
        # "images" info 
        image = create_image_annotation(original_file_name, w, h, image_id)
        images.append(image)

        sub_masks = create_sub_masks(mask_image_open, w, h)
        for color, sub_mask in sub_masks.items():
            category_id = category_colors[color]

            # "annotations" info
            polygons, segmentations = create_sub_mask_annotation(sub_mask)

            # Check if we have classes that are a multipolygon
            if category_id in multipolygon_ids:
                # Combine the polygons to calculate the bounding box and area
                multi_poly = MultiPolygon(polygons)
                                
                annotation = create_annotation_format(multi_poly, segmentations, image_id, category_id, annotation_id)

                annotations.append(annotation)
                annotation_id += 1
            else:
                for i in range(len(polygons)):
                    # Cleaner to recalculate this variable
                    segmentation = [np.array(polygons[i].exterior.coords).ravel().tolist()]
                    
                    annotation = create_annotation_format(polygons[i], segmentation, image_id, category_id, annotation_id)
                    
                    annotations.append(annotation)
                    annotation_id += 1
        image_id += 1
    return images, annotations, annotation_id

if __name__ == "__main__":
  main()

# # # END OF create-custom-coco-dateset.ipynb IN ORIGINAL REPO. 
