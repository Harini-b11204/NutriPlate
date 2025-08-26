# Main pipeline entry point
from detection.detector import detect_food
from classification.classifier import classify_food
from freshness.freshness import estimate_freshness
from nutrition.nutrition import get_nutrition

# Example usage
if __name__ == "__main__":
    image_path = "data/sample_plate.jpg"
    detected_items = detect_food(image_path)
    results = []
    for item in detected_items:
        food_type = classify_food(item['image'])
        portion = item['portion']
        freshness = estimate_freshness(item['image'])
        nutrition = get_nutrition(food_type, portion)
        results.append({
            "food": food_type,
            "portion": portion,
            "freshness": freshness,
            "nutrition": nutrition
        })
    print(results)
