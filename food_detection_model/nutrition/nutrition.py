# Nutrition lookup stub
def get_nutrition(food_type, portion):
    # Expanded nutrition info for common foods
    food_db = {
        "apple": {"calories": 95, "macros": {"carbs": 25, "protein": 0.5, "fat": 0.3}, "micros": {"vitamin_c": "8.4mg", "potassium": "195mg"}},
        "banana": {"calories": 105, "macros": {"carbs": 27, "protein": 1.3, "fat": 0.3}, "micros": {"vitamin_c": "10.3mg", "potassium": "422mg"}},
        "pizza": {"calories": 285, "macros": {"carbs": 36, "protein": 12, "fat": 10}, "micros": {"calcium": "189mg", "iron": "2.5mg"}},
        "hotdog": {"calories": 151, "macros": {"carbs": 2, "protein": 5, "fat": 13}, "micros": {"sodium": "567mg", "iron": "0.8mg"}},
        "hamburger": {"calories": 250, "macros": {"carbs": 31, "protein": 12, "fat": 9}, "micros": {"iron": "2.2mg", "potassium": "270mg"}},
        "ice cream": {"calories": 137, "macros": {"carbs": 16, "protein": 2.3, "fat": 7.3}, "micros": {"calcium": "84mg", "vitamin_a": "278IU"}},
        "carrot": {"calories": 25, "macros": {"carbs": 6, "protein": 0.6, "fat": 0.1}, "micros": {"vitamin_a": "835mcg", "potassium": "195mg"}},
        "broccoli": {"calories": 55, "macros": {"carbs": 11, "protein": 3.7, "fat": 0.6}, "micros": {"vitamin_c": "89mg", "calcium": "47mg"}},
        "orange": {"calories": 62, "macros": {"carbs": 15.4, "protein": 1.2, "fat": 0.2}, "micros": {"vitamin_c": "70mg", "potassium": "237mg"}},
        "strawberry": {"calories": 4, "macros": {"carbs": 0.9, "protein": 0.1, "fat": 0.0}, "micros": {"vitamin_c": "7mg", "potassium": "18mg"}},

        # Grains & staples
        "rice": {"calories": 206, "macros": {"carbs": 45, "protein": 4.3, "fat": 0.4}, "micros": {"iron": "1.9mg"}},
        "pasta": {"calories": 221, "macros": {"carbs": 43, "protein": 8, "fat": 1.3}, "micros": {"iron": "1.3mg"}},
        "bread": {"calories": 79, "macros": {"carbs": 14, "protein": 3, "fat": 1.0}, "micros": {"iron": "0.7mg"}},
        "bagel": {"calories": 245, "macros": {"carbs": 47, "protein": 9, "fat": 1.5}, "micros": {}},
        "oatmeal": {"calories": 158, "macros": {"carbs": 27, "protein": 6, "fat": 3.2}, "micros": {"fiber": "4g"}},
        "quinoa": {"calories": 120, "macros": {"carbs": 21, "protein": 4.4, "fat": 1.9}, "micros": {}},

        # Proteins
        "chicken": {"calories": 165, "macros": {"carbs": 0, "protein": 31, "fat": 3.6}, "micros": {"iron": "1mg"}},
        "beef": {"calories": 250, "macros": {"carbs": 0, "protein": 26, "fat": 15}, "micros": {"iron": "2.6mg"}},
        "pork": {"calories": 242, "macros": {"carbs": 0, "protein": 27, "fat": 14}, "micros": {}},
        "salmon": {"calories": 206, "macros": {"carbs": 0, "protein": 22, "fat": 12}, "micros": {"omega_3": "2260mg"}},
        "tuna": {"calories": 132, "macros": {"carbs": 0, "protein": 28, "fat": 1}, "micros": {"omega_3": "233mg"}},
        "cod": {"calories": 82, "macros": {"carbs": 0, "protein": 18, "fat": 0.7}, "micros": {}},
        "shrimp": {"calories": 99, "macros": {"carbs": 0.2, "protein": 24, "fat": 0.3}, "micros": {}},
        "tofu": {"calories": 76, "macros": {"carbs": 1.9, "protein": 8, "fat": 4.8}, "micros": {"calcium": "350mg"}},
        "beans": {"calories": 127, "macros": {"carbs": 22.8, "protein": 8.7, "fat": 0.5}, "micros": {"iron": "2.1mg"}},

        # Vegetables
        "spinach": {"calories": 23, "macros": {"carbs": 3.6, "protein": 2.9, "fat": 0.4}, "micros": {"vitamin_k": "482mcg"}},
        "lettuce": {"calories": 5, "macros": {"carbs": 1, "protein": 0.5, "fat": 0.1}, "micros": {}},
        "cucumber": {"calories": 8, "macros": {"carbs": 1.9, "protein": 0.3, "fat": 0.1}, "micros": {}},
        "mushroom": {"calories": 22, "macros": {"carbs": 3.3, "protein": 3.1, "fat": 0.3}, "micros": {}},
        "potato": {"calories": 163, "macros": {"carbs": 37, "protein": 4.3, "fat": 0.2}, "micros": {}},
        "sweet potato": {"calories": 86, "macros": {"carbs": 20, "protein": 1.6, "fat": 0.1}, "micros": {"vitamin_a": "14187IU"}},

        # Dairy & eggs
        "egg": {"calories": 78, "macros": {"carbs": 0.6, "protein": 6.3, "fat": 5.3}, "micros": {"vitamin_b12": "0.6mcg"}},
        "milk": {"calories": 122, "macros": {"carbs": 12, "protein": 8, "fat": 5}, "micros": {"calcium": "300mg"}},
        "cheese": {"calories": 113, "macros": {"carbs": 0.4, "protein": 7, "fat": 9}, "micros": {"calcium": "200mg"}},
        "yogurt": {"calories": 59, "macros": {"carbs": 3.6, "protein": 10, "fat": 0.4}, "micros": {}},

        # Snacks & desserts
        "chocolate": {"calories": 546, "macros": {"carbs": 61, "protein": 4.9, "fat": 31}, "micros": {}},
        "cookie": {"calories": 78, "macros": {"carbs": 10, "protein": 1, "fat": 3.5}, "micros": {}},
        "pancake": {"calories": 86, "macros": {"carbs": 12, "protein": 2, "fat": 3}, "micros": {}},

        # Beverages (per typical serving)
        "coffee": {"calories": 2, "macros": {"carbs": 0, "protein": 0.3, "fat": 0}, "micros": {}},
        "orange juice": {"calories": 112, "macros": {"carbs": 26, "protein": 1.7, "fat": 0.5}, "micros": {"vitamin_c": "124mg"}},
        "soda": {"calories": 150, "macros": {"carbs": 39, "protein": 0, "fat": 0}, "micros": {}},

        # Misc
        "sushi": {"calories": 200, "macros": {"carbs": 28, "protein": 8, "fat": 5}, "micros": {}},
        "fried rice": {"calories": 238, "macros": {"carbs": 34, "protein": 6, "fat": 8}, "micros": {}},
        "naan": {"calories": 260, "macros": {"carbs": 49, "protein": 8, "fat": 4}, "micros": {}},
    }
    # Filter out non-food predictions
    non_food = ["plate", "spoon", "fork", "knife", "bowl", "cup", "table", "napkin"]
    if food_type.lower() in non_food:
        return {"calories": 0, "macros": {}, "micros": {}}
    # Add common meats and staples with approximate per-serving values
    extra = {
        "chicken": {"calories": 165, "macros": {"carbs": 0, "protein": 31, "fat": 3.6}, "micros": {"iron": "1mg", "potassium": "256mg"}},
        "chicken_breast": {"calories": 165, "macros": {"carbs": 0, "protein": 31, "fat": 3.6}, "micros": {"iron": "1mg", "potassium": "256mg"}},
        "beef": {"calories": 250, "macros": {"carbs": 0, "protein": 26, "fat": 15}, "micros": {"iron": "2.6mg", "zinc": "5.1mg"}},
        "pork": {"calories": 242, "macros": {"carbs": 0, "protein": 27, "fat": 14}, "micros": {"thiamin": "0.8mg", "iron": "0.9mg"}},
        "salmon": {"calories": 206, "macros": {"carbs": 0, "protein": 22, "fat": 12}, "micros": {"omega_3": "2260mg", "vitamin_d": "447IU"}},
        "tuna": {"calories": 132, "macros": {"carbs": 0, "protein": 28, "fat": 1}, "micros": {"omega_3": "233mg", "vitamin_d": "156IU"}},
        "egg": {"calories": 78, "macros": {"carbs": 0.6, "protein": 6.3, "fat": 5.3}, "micros": {"vitamin_b12": "0.6mcg", "vitamin_d": "44IU"}},
        "rice": {"calories": 206, "macros": {"carbs": 45, "protein": 4.3, "fat": 0.4}, "micros": {"iron": "1.9mg", "folate": "58mcg"}},
        "pasta": {"calories": 221, "macros": {"carbs": 43, "protein": 8, "fat": 1.3}, "micros": {"iron": "1.3mg", "folate": "90mcg"}},
        "tofu": {"calories": 76, "macros": {"carbs": 1.9, "protein": 8, "fat": 4.8}, "micros": {"calcium": "350mg", "iron": "1.6mg"}},
        "beans": {"calories": 127, "macros": {"carbs": 22.8, "protein": 8.7, "fat": 0.5}, "micros": {"iron": "2.1mg", "fiber": "6g"}}
    }
    # Merge extra into food_db (preserve earlier entries)
    for k, v in extra.items():
        if k not in food_db:
            food_db[k] = v

    # Normalize name (simple mapping)
    name_map = {
        'chicken breast': 'chicken_breast',
        'roast chicken': 'chicken',
        'grilled chicken': 'chicken',
        'fried chicken': 'chicken',
        'steak': 'beef',
        'ground beef': 'beef',
        'pork chop': 'pork',
        'salmon fillet': 'salmon',
        'tuna steak': 'tuna',
        'egg (fried)': 'egg',
        'egg (boiled)': 'egg',
        'white rice': 'rice',
        'brown rice': 'rice',
        'spaghetti': 'pasta',
        'mac and cheese': 'pasta',
        'tofu (firm)': 'tofu',
        'baked beans': 'beans'
    }
    key = food_type.lower()
    if key in name_map:
        key = name_map[key]

    # Portion scaling: small=0.5, medium=1, large=1.5
    portion_factors = {'small': 0.5, 'medium': 1.0, 'large': 1.5}
    factor = portion_factors.get(str(portion).lower(), 1.0)

    entry = food_db.get(key)
    if not entry:
        return {"calories": 0, "macros": {}, "micros": {}}

    # Scale numeric macros/calories by portion factor
    scaled_macros = {}
    for m, val in entry.get('macros', {}).items():
        try:
            scaled_macros[m] = round(val * factor, 2)
        except Exception:
            scaled_macros[m] = val
    scaled_micros = entry.get('micros', {})
    try:
        scaled_calories = int(entry.get('calories', 0) * factor)
    except Exception:
        scaled_calories = entry.get('calories', 0)

    return {"calories": scaled_calories, "macros": scaled_macros, "micros": scaled_micros}
