import requests

class FoodData:
    apiKey = 'LW4opyxo9Yi7OQomJPbFjLj70r7wreqHM2zLMYzr'
    baseUrl = 'https://api.nal.usda.gov/fdc/v1/foods/search'

    def getItems(searchQuery: str, pageSize: int = 30) -> list:
        """Sends request to Food Data Central api and returns information about foods related to search query

        Args:
            searchQuery (string): Name of food that user is searching for 
            pageSize (int): Number of items returned 

        Returns:
            list: [{
                        foodName: string, 
                        servingSize: {value: float, unit: string}, 
                        nutrients: {
                                    carbohydrates: {value: float, unit: string}, 
                                    fat: {value: float, unit: string}, 
                                    protein: {value: float, unit: string}, 
                                    calories: {value: float, unit: string}
                                }
                }] 
        """

        response = requests.get(FoodData.baseUrl, params={
                                'query': searchQuery, 'pageSize': pageSize, 'api_key': FoodData.apiKey}).json()
        foods = response['foods']
        output = []

        if len(foods) > 1:
            for food in foods:
                foodName = food.get('lowercaseDescription')
                brand = food.get('brandName')
                servingSize = food.get('servingSize')
                servingUnit = food.get('servingSizeUnit')
                nutrients = food.get('foodNutrients')

                nutrientData = {}

                # extract nutrient data
                for nutrient in nutrients:
                    name = nutrient['nutrientName']

                    # check if nutrient is one of the ones that I want to display
                    # example of abstraction since some values such as the amount of cholestrol and vitamin c are not included
                    if 'protein' in name.lower():
                        name = 'protein'
                    elif 'fat' in name.lower():
                        name = 'fat'
                    elif 'carbohydrate' in name.lower():
                        name = 'carbohydrates'
                    elif 'energy' in name.lower():
                        name = 'calories'
                    else:
                        name = None

                    if name:
                        unit = nutrient['unitName']
                        value = nutrient['value']
                        nutrientData[name] = {
                            'value': float(value), 'unit': unit}

                output.append({
                    'foodName': f'{foodName} by {brand}' if brand else foodName,
                    'servingSize': {'value': servingSize if servingSize else 1, 'unit': servingUnit if servingUnit else 'item'},
                    'nutrients': nutrientData
                })

            return output
        else:
            return 'No results found'
        
    def searchByBarcode(barcode: str):
        """Uses openfoodfacts api to get information about food item through its barcode

        Args:
            barcode (str): barcode of the food item being searched for

        Returns:
            dict({
                    foodName: string, 
                    servingSize: {value: float, unit: string}, 
                    nutrients: {
                                    carbohydrates: {value: float, unit: string}, 
                                    fat: {value: float, unit: string}, 
                                    protein: {value: float, unit: string}, 
                                    calories: {value: float, unit: string}
                                }
                })
            
            
        """        
        url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}'
        response = requests.get(url)
        
        if response.status_code == 200:
            responseData = response.json()
            output = {}
            
            nutrients = responseData['product']['nutriments']
            servingSize = responseData['product']['nutrition_data_per']
            productName = responseData['product']['product_name']
            
            output = {
                        'foodName': productName, 
                        'servingSize': {'value': float(servingSize[:-1]), 'unit': servingSize[-1]}, 
                        'nutrients': {
                            nutrient if nutrient != 'energy' else 'calories': 
                                {'value' : nutrients[nutrient], 'unit': nutrients[f'{nutrient}_unit']}
                            for nutrient in ['carbohydrates', 'proteins', 'fat', 'energy']
                        }
                     }
            
            return output
        else:
            return 'Error'
        


if __name__ == '__main__':
    print(FoodData.getItems('Tuna'))
    print(FoodData.searchByBarcode('8711000363768'))
