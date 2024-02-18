
import csv

# CREDIT: ChatGPT 
def export_dict_to_csv(data, filename):
    """
    Export a dictionary to a CSV file.
    
    Parameters:
    - data: Dictionary to export
    - filename: Name of the CSV file to create
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
  freqs = {'background': 9158, 'apple': 79, 'sauce': 419, 'strawberry': 389, 'blueberry': 219, 'pie': 257, 'fish': 135, 'corn': 167, 'potato': 406, 'pork': 269, 'bread': 739, 'tomato': 689, 'lettuce': 346, 'pepper': 243, 'cheese butter': 210, 'steak': 475, 'cilantro mint': 491, 'onion': 305, 'french fries': 92, 'chicken duck': 511, 'cucumber': 267, 'lemon': 262, 'garlic': 28, 'carrot': 668, 'celery stick': 91, 'avocado': 33, 'grape': 47, 'juice': 65, 'banana': 100, 'pineapple': 76, 'orange': 110, 'other ingredients': 113, 'broccoli': 441, 'mango': 25, 'rice': 287, 'lamb': 37, 'sausage': 94, 'watermelon': 19, 'noodles': 144, 'French beans': 178, 'spring onion': 116, 'ice cream': 419, 'asparagus': 148, 'green beans': 124, 'egg': 112, 'cake': 231, 'coffee': 61, 'raspberry': 59, 'pizza': 29, 'kiwi': 25, 'bean sprouts': 22, 'dried cranberries': 55, 'walnut': 82, 'cabbage': 41, 'pasta': 60, 'soup': 31, 'fried meat': 119, 'milk': 37, 'almond': 71, 'biscuit': 130, 'milkshake': 32, 'peach': 31, 'seaweed': 10, 'cherry': 144, 'shrimp': 92, 'soy': 18, 'chocolate': 62, 'tofu': 37, 'rape': 22, 'pear': 19, 'ginger': 12, 'tea': 6, 'hamburg': 1, 'cauliflower': 100, 'shiitake': 103, 'red beans': 29, 'snow peas': 51, 'wine': 50, 'shellfish': 29, 'cashew': 42, 'olives': 43, 'wonton dumplings': 10, 'crab': 10, 'melon': 7, 'enoki mushroom': 5, 'white radish': 31, 'fig': 9, 'white button mushroom': 62, 'kelp': 6, 'king oyster mushroom': 3, 'hanamaki baozi': 12, 'salad': 11, 'pumpkin': 25, 'eggplant': 9, 'popcorn': 11, 'apricot': 18, 'okra': 10, 'bamboo shoots': 7, 'candy': 44, 'peanut': 20, 'date': 3, 'egg tart': 6, 'pudding': 1, 'oyster mushroom': 4}
  export_dict_to_csv(freqs, "output.csv")
