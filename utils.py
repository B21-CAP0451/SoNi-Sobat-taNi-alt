import tensorflow as tf
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions

def predict_json(region, instances, version=None):

    # Create the ML Engine service object
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)

    # Setup model path
    model_path = "projects/<project_id>/models/<model_name>"
    if version is not None:
        model_path += "/versions/{}".format(version)

    # Create ML engine resource endpoint and input data
    ml_resource = googleapiclient.discovery.build(
        "ml", "v1", cache_discovery=False, client_options=client_options).projects()
    instances_list = instances.numpy().tolist() # turn input into list (ML Engine wants JSON)
    
    input_data_json = {"signature_name": "serving_default",
                       "instances": instances_list} 

    request = ml_resource.predict(name=model_path, body=input_data_json)
    response = request.execute()
    
    if "error" in response:
        raise RuntimeError(response["error"])

    return response["predictions"]

# function to import an image and resize it to be able to be used with our model
def load_and_prep_image(filename, img_shape=224, rescale=False):
 
  img = tf.io.decode_image(filename, channels=3) # make sure there's 3 colour channels (for PNG's)
  # Resize the image
  img = tf.image.resize(img, [img_shape, img_shape])
  # Rescale the image (get all values between 0 and 1)
  if rescale:
      return img/255.
  else:
      return img