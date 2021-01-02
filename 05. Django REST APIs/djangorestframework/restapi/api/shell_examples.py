# Serialization - The process of converting data from django models to a stream of bytes or to a native python data structure or object

# Create a Serialization class in the serializers.py file
>> from api.models import Posts
>> from api.serializers import PostSerializer

# Get a QuerySet
.> obj = Posts.objects.all()
# To serialize this query set using the created serializer class 
>> json_data = PostSerializer(obj, many = True)  # many is set to True if there are multiple instances
# The json_data is a python dictionary or array of dictionaries

# To render to JSON data
>> from rest_framework.renderers import JSONRenderer
>> json_data_rendered = JSONRenderer().render(json_data.data) # Converts to a stream of bytes 

# To deserialize
>> import io
>> from rest_framework.parsers import JSONParser

>> data = io.BytesIO(json_data_rendered)
>> deserialized_data = JSONParser().parse(data) # Returns the deserialized data 

## Create Object Serializer 
obj = Posts.objects.all()
data = {"user":1, "content": "I hate this Life !, Fuck us all."}
create_obj_serializer = PostSerializer(data = data)
create_obj_serializer.is_valid()
if create_obj_serializer.is_valid():
    create_obj_serializer.save()


## Update Object Serializer 
obj = Posts.objects.get(id = 4)
data = {"user":1, "content":"Okay, that was quite harsh. Let's all pray for God's goodness !"}
update_obj_serializer = PostSerializer(obj, data = data)
update_obj_serializer.is_valid()
if update_obj_serializer.is_valid():
    update_obj_serializer.save()