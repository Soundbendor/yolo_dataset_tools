
import os 
from .annotation import Annotation 
from shutil import copyfile

def _convert_image_path_to_label_path(image_path) -> str:
  image_path = "labels".join(image_path.rsplit("images", 1)) # Replaces last instance of "images" in path with "labels".
  return ".".join(image_path.split(".")[:-1]) + ".txt"

class Image:
  def __init__(self, image_abs_path, category_id_to_name_dict):
    """
    Assumes corresponding label follows YOLO format-- replaces "images" 
    in image_abs_path with "labels" and uses ".txt" file ending to find label path. 
    """
    self._image_abs_path = image_abs_path
    self._category_id_to_name_dict = category_id_to_name_dict # Local dataset mapping. 

  def write(self, image_write_abs_path, annotation_write_abs_path, category_name_to_id_dict, *, overwrite=False) -> bool:
    if not overwrite and (os.path.exists(image_write_abs_path) or os.path.exists(annotation_write_abs_path)):
      return False 

    self._write_image(image_write_abs_path)
    Annotation.write_annotation_list(annotation_write_abs_path, self.annotation_list, category_name_to_id_dict, overwrite=overwrite) # Global dataset mapping. 
    return True
  
  @property
  def image_basename(self) -> str:
    return os.path.basename(self.image_path)

  @property
  def label_basename(self) -> str:
    return os.path.basename(self.label_path)

  
  
  @property
  def image_path(self) -> str:
    return self._image_abs_path

  @property 
  def label_path(self) -> str:
    return _convert_image_path_to_label_path(self.image_path)

  @property
  def annotation_list(self) -> list[Annotation]:
    return Annotation.from_path(self.label_path, self._category_id_to_name_dict)  
  
  def _write_image(self, image_write_abs_path):
    os.makedirs(os.path.dirname(image_write_abs_path), exist_ok=True)
    copyfile(self.image_path, image_write_abs_path)
  