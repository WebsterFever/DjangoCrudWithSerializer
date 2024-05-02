from rest_framework.views import Request, Response, APIView , status

from ingredients.models import Ingredient
from .models import Recipe
from .serializers import RecipeSerializer



class RecipeView(APIView):
    def post(self, req: Request) -> Response:
        serializer = RecipeSerializer(data=req.data)
       # if not serializer.is_valid():
            #return Response(
              #  serializer.errors,
              #  status.HTTP_400_BAD_REQUEST,
            #)
        serializer.is_valid(raise_exception=True)
        ingredients = serializer.validated_data.pop("ingredients")    
        recipe = Recipe.objects.create(**serializer.validated_data)

        for ingredient_data in ingredients:
          #  try:
            ingredient = Ingredient.objects.filter(name__iexact=ingredient_data["name"])
            if not ingredient:
                ingredient = Ingredient.objects.create(**ingredient_data)
            else: 
                ingredient = ingredient.first()
                recipe.ingredients.add(ingredient)
           # except Ingredient.DoesNotExist:      

        serializer = RecipeSerializer(recipe)
        return Response(serializer.data , status.HTTP_201_CREATED)