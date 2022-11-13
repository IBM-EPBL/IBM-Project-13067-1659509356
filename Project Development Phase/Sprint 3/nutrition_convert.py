import pickle


Nutrition_file_obj = open('Nutrition.p','wb')


Nutrition = {}

Nutrition["Apple"] = {
    "Calories": "52",
    "Water" : "86%",
    "Protein": "0.3 grams",
    "Carbs": "13.8 grams",
    "Sugar": "10.4 grams",
    "Fiber": "2.4 grams",
    "Fat": "0.2 grams"
}

Nutrition["Orange"] =  {
        "Calories": "66",
        "Water": "86%" ,
        "Protein" : "1.3 grams",
        "Carbs": "14.8 grams",
        "Sugar": "12 grams",
        "Fiber": "2.8 grams",
        "Fat": "0.2 grams",
        "Vitamin C": "92% of the Daily Value (DV)",
        "Folate": "9% of the DV",
        "Calcium": "5% of the DV",
        "Potassium": "5% of the DV"
}

Nutrition["Banana"] = {
    "Calories": "89",
    "Water": "75%",
    "Protein": "1.1 grams",
    "Carbs": "22.8 grams",
    "Sugar": "12.2 grams",
    "Fiber": "2.6 grams",
    "Fat": "0.3 grams"
}

Nutrition["Pineapple"] = {
    "Calories": "83",
    "Fat": "1.7 grams",
    "Protein": "1 gram",
    "Carbs": "21.6 grams",
    "Fiber": "2.3 grams",
    "Vitamin C": "88% of the Daily Value (DV)",
    "Manganese": "109% of the DV",
    "Vitamin B6": "11% of the DV",
    "Copper": "20% of the DV",
    "Thiamine": "11% of the DV",
    "Folate": "7% of the DV",
    "Potassium": "4% of the DV",
    "Magnesium": "5% of the DV",
    "Niacin": "5% of the DV",
    "Pantothenic acid": "7% of the DV",
    "Riboflavin": "4% of the DV",
    "Iron": "3% of the DV"
}

Nutrition["Watermelon"] = {
    "Calories": "30",
    "Water": "91%",
    "Protein": "0.6 grams",
    "Carbs": "7.6 grams",
    "Sugar": "6.2 grams",
    "Fiber": "0.4 grams",
    "Fat": "0.2 grams"
}

pickle.dump(Nutrition, Nutrition_file_obj)

Nutrition_file_obj.close()

Nutrition_file_obj_t = open('Nutrition.p','rb')

n1 = pickle.load(Nutrition_file_obj_t)

Nutrition_file_obj_t.close()

print(n1["Apple"])






