from rest_framework import serializers

from product.models import Category, SubCategory, Product


class AddProductSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    sub_category = serializers.CharField(required=True, max_length=100)
    category = serializers.CharField(write_only=True ,max_length=100)

    def create(self, validated_data):
        existing_category = Category.objects.filter(name=validated_data["category"]).first()

        if existing_category:
            existing_sub_category_for_category = SubCategory.objects.filter(name=validated_data["sub_category"], category=existing_category).first()

            if not existing_sub_category_for_category:
                new_sub_category = SubCategory.objects.create(name=validated_data["sub_category"], category=existing_category)
                instance = Product.objects.create(name=validated_data["name"], sub_category=new_sub_category)

            else:
                existing_product_for_same_category_and_sub_category = Product.objects.filter(name=validated_data["name"], sub_category=existing_sub_category_for_category).first()

                if not existing_product_for_same_category_and_sub_category:
                    instance = Product.objects.create(name=validated_data["name"], sub_category=existing_sub_category_for_category)

                else:
                    raise serializers.ValidationError("Same product with same sub category and same category not allowed")

        else:
            new_category = Category.objects.create(name=validated_data["category"])
            new_sub_category = SubCategory.objects.create(name=validated_data["sub_category"], category=new_category)
            instance = Product.objects.create(name=validated_data["name"], sub_category=new_sub_category)

        return instance