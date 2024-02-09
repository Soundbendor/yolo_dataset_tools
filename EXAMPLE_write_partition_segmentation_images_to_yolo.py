
from yolo_dataset_tools import write_partition_segmentation_images_to_yolo, get_category_list_from_file

if __name__ == "__main__":
  FOOD_SEG_103_TEST_ORIG_IMAGES_PATH  = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/Test/images/"
  FOOD_SEG_103_TEST_LABEL_IMAGES_PATH = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/Test/labels_images/"
  FOOD_SEG_103_JSON_WRITE_PATH        = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/Test/coco_json/test_json_write_path.json"
  FOOD_SEG_103_YOLO_FOLDER_PATH       = "/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/yolo/"
  FOOD_SEG_103_CATEGORY_ID_MAP        = get_category_list_from_file("/home/joey/food-waste-model-training/datasets/datasets/Food_Seg_103/FoodSeg103/category_id.txt", start_line=0)
  FOOD_SEG_103_PARTITION              = "test"
  LIMIT                               = None 
  ASK_OVERWRITE                       = True 
  PRINT_PROGRESS                      = "print" 
  write_partition_segmentation_images_to_yolo(
    FOOD_SEG_103_TEST_ORIG_IMAGES_PATH,
    FOOD_SEG_103_TEST_LABEL_IMAGES_PATH,
    FOOD_SEG_103_JSON_WRITE_PATH,
    FOOD_SEG_103_YOLO_FOLDER_PATH,
    FOOD_SEG_103_PARTITION,
    FOOD_SEG_103_CATEGORY_ID_MAP,
    LIMIT,
    ask_overwrite=ASK_OVERWRITE,
    print_progress=PRINT_PROGRESS,
  )
