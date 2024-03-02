
from copy import deepcopy 

def remove_background(coco_dict) -> dict:
  """ Returns new dict without "background" annotations. """
  coco_dict = deepcopy(coco_dict)
  coco_dict["annotations"] = [annotation for annotation in coco_dict["annotations"] if annotation["category_id"] != 0]
  for i in range(len(coco_dict["annotations"])):
    coco_dict["annotations"][i]["category_id"] -= 1
  if not coco_dict["categories"][0]["name"] == "background":
    raise Exception("Attempted to remove 'background' category but it was not first category in categories list.")
  coco_dict["categories"] = coco_dict["categories"][1:]
  for i in range(len(coco_dict["categories"])):
    coco_dict["categories"][i]["id"] -= 1
  return coco_dict
