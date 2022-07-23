import requests


# TODO: Add data type control 


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
                        name: str
                        servingSize: dict
                        nutrients: dict
                }] 
        """
        
                
        response = requests.get(FoodData.baseUrl, params={'query': searchQuery, 'pageSize': pageSize, 'api_key': FoodData.apiKey}).json()
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
                        nutrientData[name] = {'value': float(value), 'unit': unit}
                        
                
                output.append({
                    'foodName': f'{foodName} by {brand}' if brand else foodName, 
                    'servingSize': {'value': servingSize if servingSize else 1, 'unit': servingUnit if servingUnit else 'item'}, 
                    'nutrients': nutrientData
                })
                
            return output
        else:
            return 'No results found'



if __name__ == '__main__':
    print(FoodData.getItems('onions raw'))
    