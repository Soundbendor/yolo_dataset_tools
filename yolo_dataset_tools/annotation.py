
from typing import Any 
from operator import attrgetter
import os 

CategoryName = str 
""" Name, not ID. """

PropCoord = float 
""" Typically in [0., 1.]. """

class Annotation:
  def __init__(self, category: CategoryName, segmentation_list: list[PropCoord]):
    self._category = category
    self._segmentation_list = list(segmentation_list)

  def as_str(self, name_to_id_map: dict) -> str:
    return f"{name_to_id_map[self.category]} {' '.join(str(coord) for coord in self._segmentation_list)}"

  def __repr__(self) -> str:
    return f"Annotation(category={self.category}, segmentation_list={self.segmentation_list})"

  @property
  def category(self) -> str:
    return self._category
  
  @property
  def segmentation_list(self) -> list[PropCoord]:
    return list(self._segmentation_list)
  
  def __getitem__(self, key) -> Any:
    return attrgetter(key)(self)
    
  @staticmethod 
  def from_path(path, id_to_name_dict) -> list["Annotation"]:
    return [ Annotation._from_line(line, id_to_name_dict) for line in open(path, "r").readlines() ]

  @staticmethod
  def _from_line(line, id_to_name_dict) -> "Annotation":
    category = id_to_name_dict[int(line.split(" ")[0])]
    segmentation_list = [PropCoord(coord) for coord in line.split(" ")[1:]]
    return Annotation(category, segmentation_list)
    
  @staticmethod
  def write_annotation_list(write_path, annotation_list, name_to_id_dict, *, overwrite=False) -> bool:
    """ Returns whether wrote. If path already exists, does not write. """
    # Converting write_path to absolute path. 
    write_path = os.path.abspath(write_path)
    if not os.path.exists(write_path) or overwrite:
      if not os.path.exists(os.path.dirname(write_path)):
        os.makedirs(os.path.dirname(write_path))
      with open(write_path, "w") as f:
        f.write("\n".join(annotation.as_str(name_to_id_dict) for annotation in annotation_list))
      return True
    else:
      return False

if __name__ == "__main__":
  annotation = Annotation("test_category_name", [0., 0.25, 0.5, 0.75])
  print(annotation)
  print(Annotation.write_annotation_list("test_annotation_write.txt", [annotation] * 3, {"test_category_name": "test_category_ID"}, overwrite=False))
  
  """
  Result in test_annotation_write.txt: 
  test_category_ID 0.0 0.25 0.5 0.75
  test_category_ID 0.0 0.25 0.5 0.75
  test_category_ID 0.0 0.25 0.5 0.75
  """
  