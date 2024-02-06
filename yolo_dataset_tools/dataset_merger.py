
from .dataset import Dataset 
import bidict, json, os 

"""
DatasetMerger: 
- TL;DR: Streamlines merging multiple datasets into a folder. 
- Interface: 
  - add(name, yaml_path) 
  - add_reduction(primary, secondary_list) 
- Handles writing annotations with new IDs + metadata JSON. 
  - Writes according to global ID map of DatasetMerger. 
  - Uses category names, rather than categories, and ignores local IDs. 
  - Auto-stores metadata as JSON. (Dataset names/YAML paths, global name-to-ID map, 
    global category reductions.) 
- Provides interface for category reductions. 
  - I.e., IDs of multiple category names are merged into the ID of a single category name. 
  - Multiple category name IDs merging from => secondary category names. 
  - Single category name ID merging to      => primary category name. 
"""

PrimaryCategoryName = SecondaryCategoryName = CategoryName = str 
IrreducedCategoryId = ReducedCategoryId = CategoryId   = int 

def _convert_irreduced_to_reduced(irreduced: dict[CategoryName, IrreducedCategoryId], reductions: dict[SecondaryCategoryName, PrimaryCategoryName]) -> bidict[CategoryName, ReducedCategoryId]: 
  """ Returns dictionary with irreduced CategoryIds converted to reduced CategoryIds. """
  reduced = bidict()
  for (category_name, irreduced_id) in irreduced.items():
    if category_name in reductions:
      reduced[category_name] = irreduced[reductions[category_name]]
    else:
      reduced[category_name] = reductions[category_name]
  return reduced 

class DatasetMerger:
  def __init__(self, json_path, folder_path):
    if not os.path.exists(json_path):
      self.json_path = json_path
      self.folder_path = folder_path
      
      self.datasets = {}
      self.irreduced_global_name_to_id_dict = bidict()
      self.category_secondary_to_primary_reductions = {}
    else:
      self._load_from_json(json_path)
      
  def add(self, name, yaml_path, *, overwrite=False): 
    """ Adds dataset to folder and JSON metadata. """
    dataset = Dataset(name, yaml_path) 
    self.datasets[name] = yaml_path 
    self._add_categories(dataset.category_id_to_name_dict.values())
    dataset.write(self.folder_path, self.reduced_global_name_to_id_dict, overwrite=overwrite)
    self.save()
    
  def save(self):
    if not os.path.exists(os.path.dirname(self.json_path)):
      os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
    dct = {
      "json_path": self.json_path,
      "folder_path": self.folder_path,
      
      "datasets": self.datasets,
      "irreduced_global_name_to_id_dict": dict(self.irreduced_global_name_to_id_dict),
      "category_secondary_to_primary_reductions": self.category_secondary_to_primary_reductions,
    }
    with open(self.json_path, "w") as f:
      json.dump(dct, f)
      
  def add_reduction(self, primary, secondary_list, *, overwrite=False):
    """ Adds reduction from secondary or list of secondaries to primary. """
    for secondary in secondary_list:
      if overwrite or (secondary not in self.category_secondary_to_primary_reductions):
        self.category_secondary_to_primary_reductions[secondary] = primary
      
  @property
  def reduced_global_name_to_id_dict(self) -> bidict[CategoryName, ReducedCategoryId]:
    """ Returns with the secondary IDs replaced with primary IDs. """
    return _convert_irreduced_to_reduced(self.irreduced_global_name_to_id_dict, self.category_secondary_to_primary_reductions)
  
  @property 
  def category_primary_to_secondary_reductions(self) -> dict[PrimaryCategoryName, set[SecondaryCategoryName]]:
    """ Returns { primary_name1 => { secondary_name1, secondary_name2, ...}, ... }. """
    dct = defaultdict(set)
    for (primary, secondary) in self.category_secondary_to_primary_reductions.items():
      dct[secondary].add(primary)
    return dct

  def _add_categories(self, category_name_list):
    for category_name in category_name_list:
      self._add_category(category_name)

  def _add_category(self, category_name):
    # NOTE: Assumes that categories are never deleted. 
    if category_name not in self.irreduced_global_name_to_id_dict:
      self.irreduced_global_name_to_id_dict[category_name] = len(self.irreduced_global_name_to_id_dict)
    
  def _load_from_json(self, json_path):
    with open(json_path, "r") as f:
      dct = json.load(f) 
      
    self.json_path = dct["json_path"]
    self.folder_path = dct["folder_path"]
    
    self.datasets = dct["datasets"]
    self.irreduced_global_name_to_id_dict = bidict(dct["irreduced_global_name_to_id_dict"])
    self.category_secondary_to_primary_reductions = dct["category_secondary_to_primary_reductions"]
    