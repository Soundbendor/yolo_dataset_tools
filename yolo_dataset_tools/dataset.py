
import yaml, bidict, os, glob 
from collections import defaultdict 

class Dataset:
  def __init__(self, name, yaml_path):
    self._name = name
    self._yaml_path = yaml_path
    """
    YAML file has: 
    - path
    - train
    - val
    - test (optional) 
    - names (dict of index => category name) 
    """
    
  def write(self, write_folder, global_category_name_to_id_dict, partition="all", *, overwrite=False):
    """ partition = "all" | "train" | "val" | "test" """
    if partition == "all":
      partitions = ["train", "val", "test"]
    else:
      partitions = [partition]

    for partition in partitions:
      if partition in self.yaml_dict:
        self._write_partition(write_folder, global_category_name_to_id_dict, partition, overwrite=overwrite)

  def freqs(self, partition="all") -> dict:
    """ Returns frequencies of each category name. If partition="all", sums partitions. """
    if partition == "all":
      partition_list = ["train", "test", "val"]
    else:
      partition_list = [partition]

    dct = defaultdict(int)
    for partition in partition_list:
      for image in self.images(partition):
        for annotation in image.annotation_list:
          dct[annotation.category] += 1
    return dct
        
  def _write_partition(self, write_folder, global_category_name_to_id_dict, partition, *, overwrite=False) -> bool:
    self._init_partition_folders(write_folder, partition)
    for image in self.images(partition):
      image.write(
        os.path.join(write_folder, "images", partition, f"{self.name}_{image.image_basename}"), 
        os.path.join(write_folder, "labels", partition, f"{self.name}_{image.label_basename}"), 
        global_category_name_to_id_dict, 
        overwrite=overwrite,
      )
        
  def images(self, partition) -> Iterable[Image]:
    """ Raises exception if partition not in yaml. """
    for image_path in glob.glob(os.path.join(os.path.dirname(self.yaml_path), self.yaml_dict["path"], self.yaml_dict[partition], "*.jpg")):
      yield Image(image_path, self.category_id_to_name_dict)
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def yaml_path(self) -> str:
    return self._yaml_path
  
  @property 
  def yaml_dict(self) -> dict:
    with open(self.yaml_path, "r") as f:
      return yaml.safe_load(f)

  @property
  def category_id_to_name_dict(self) -> bidict:
    return bidict(self.yaml_dict["names"])
  
  def _init_partition_folders(self, write_folder, partition):
    for data in ["images", "labels"]:
      os.makedirs(os.path.join(write_folder, data, partition), exist_ok=True)
