# Requirements:
- [Python](https://www.python.org/) and pip
- [Docker](https://www.docker.com/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Trained model that you can download the example model [here](https://drive.google.com/file/d/1bXCXoV5x9PCMSZdZLNgp02zmE61qqxPe/view?usp=sharing)

## Deploy Model to AI Platform
  1. Create a bucket in Google Cloud Storage
  2. Upload saved model to bucket
  3. Create service account with ML Developer Role
  4. Create new model in AI Platform
  5. Deploy new version in the model just created
## Deploy App Locally
  1. Install and Activate virtualenv

```bash
pip install virtualenv
virtualenv <virtualenv_name>
source <virtualenv_name>/bin/activate
```

  2. Install requirements.txt

```bash
pip install -r requirements.txt
```
  
  3. change for your GCP service account credentials key and region in app.py
  4. change **<project_id>** and **<model_name>** in model_path at utils.py
  5. Run app in Streamlit

```bash
streamlit run app.py
```
  
## Deploy App Into Google Cloud Run
  1. Create a dockerfile
  2. Build image using docker

```bash
docker build -t gcr.io/PROJECT-ID/APP-NAME:latest .
```

  3. Run the build to check if the server is running
    
```bash
docker run -p 8080:8080 gcr.io/PROJECT-ID/APP-NAME:latest
```

  4. If the server is running, push the build
    
```bash
docker push gcr.io/PROJECT-ID/APP-NAME:latest
```

  5. Run and deploy the app in the cloud run
    
```bash
gcloud run deploy --image gcr.io/PROJECT-ID/APP-NAME:latest --port 8080
```

  6. To allow unauthenticated invocations, add "allUsers" as a member and assign it the "Cloud Run invoker" role.

**Note**: change the **PROJECT-ID** and **APP-NAME** with your own **project id** and **app name**