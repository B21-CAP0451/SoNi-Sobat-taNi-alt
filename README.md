Requirements:
- Python and pip
  Install python from the official site (https://www.python.org/)
- Docker
  Install docker from the official site (https://www.docker.com/)
- Google Cloud SDK
  Install Google Cloud SDK from the official site (https://cloud.google.com/sdk/docs/install)
-Trained model
  download in (https://drive.google.com/file/d/1fb_xGXo9Kh3Y-7QbRI7i3Lg-iHIb3ZjN/view?usp=sharing)
Steps:
- Deploy Model to AI Platform
  1. Create a bucket in Google Cloud Storage
  2. Upload saved model to bucket
  3. Create service account with ML Developer Role
  4. Create new model in AI Platform
  5. Deploy new version in the model just created
- Deploy App Locally
  1. Install and Activate virtualenv
    - pip install virtualenv
    - virtualenv <virtualenv_name>
    - source <virtualenv_name>/bin/activate
  2. Install requirements.txt (command: pip install -r requirements.txt)
  3. Run app in Streamlit (command: streamlit run app.py)
- Deploy App Into Google Cloud Run
  1. Create a dockerfile
  2. Build image using docker (command: docker build -t gcr.io/PROJECT-ID/APP-NAME:latest .)
  3. Run the build to check if the server is running (command: docker run -p 8080:8080 gcr.io/PROJECT-ID/APP-NAME:latest)
  4. If the server is running, push the build (command: docker push gcr.io/PROJECT-ID/APP-NAME:latest)
  5. Run and deploy the app in the cloud run (command: gcloud run deploy --image gcr.io/PROJECT-ID/APP-NAME:latest --port 8080)
  6. To allow unauthenticated invocations, add "allUsers" as a member and assign it the "Cloud Run invoker" role.
  *note: change the "PROJECT-ID" and "APP-NAME" with your own "project id" and "app name"