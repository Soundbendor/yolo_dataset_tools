
import os 
from .annotation import Annotation 
from shutil import copyfile

class Image:
  def __init__(self, image_abs_path, annotation_abs_path, category_id_to_name_dict):
    self._image_abs_path = image_abs_path
    self._annotation_abs_path = annotation_abs_path
    self._category_id_to_name_dict = category_id_to_name_dict # Local dataset mapping. 

  @property
  def annotation_list(self) -> list[Annotation]:
    return Annotation.from_path(self._annotation_abs_path, self._category_id_to_name_dict)

  def write(self, image_write_abs_path, annotation_write_abs_path, category_name_to_id_dict, *, overwrite=False) -> bool:
    if not overwrite and (os.path.exists(image_write_abs_path) or os.path.exists(annotation_write_abs_path)):
      return False 

    self._write_image(image_write_abs_path)
    Annotation.write_annotation_list(annotation_write_abs_path, self.annotation_list, category_name_to_id_dict, overwrite=overwrite) # Global dataset mapping. 
    return True
  
  def _write_image(self, image_write_abs_path):
    os.makedirs(os.path.dirname(image_write_abs_path), exist_ok=True)
    copyfile(self._image_abs_path, image_write_abs_path)
  