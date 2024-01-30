
import os 

def get_category_list_from_file(path, start_line) -> list[str]:
  """
  Given start_line=0 and path to:
    0	background
    1	candy
    2	egg tart
    ...
    
  Returns: 
  [ "background", "candy", "egg tart", ... ]

  NOTE: 
    1. **Makes LOWERCASE.** 
    2. Removes extra whitespace. 
    3. Removes numbers in front of category names. 

  If start_line=1, cuts off first line of file. 
  NOTE: Make sure to use correct start_line value if using 
        list indices as category IDs. 
  """

  f = open(path, "r")
  categories = []

  for line in f.readlines()[start_line:]:
    line = " ".join(line.split())
    cat_id, *cat_name = line.split()
    cat_name = " ".join(cat_name).lower()
    categories.append(cat_name)
    
  return categories

# EXAMPLE USE: 
if __name__ == "__main__":
  DIR_PATH = os.path.dirname(os.path.realpath(__file__))
  DATASETS_PATH = os.path.join(DIR_PATH, "datasets", "datasets")
  PATHS = [
    os.path.join(DATASETS_PATH, "Food_Seg_103", "FoodSeg103", "category_id.txt"),
    os.path.join(DATASETS_PATH, "UEC_Foodpix_Complete", "UECFOODPIXCOMPLETE", "data", "category.txt")
  ]
  lst1 = get_categories(PATHS[0])
  lst2 = get_categories(PATHS[1], 1)
  # Finding categories that BOTH datasets share. 
  set1 = set(lst1)
  set2 = set(lst2)
  inter = set1.intersection(set2)
  print("lst 1:", lst1)
  print("lst 2:", lst2)
  print("Inter:", inter)
