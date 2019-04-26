# easy_retrain-object_detection
Make object detection easier

Docker Image from this tutorial -> https://coral.withgoogle.com/docs/edgetpu/retrain-detection/

### Create the Docker image
docker build - < Dockerfile --tag detect-tutorial

### Run the docker image
``docker run --name edgetpu-detect --rm -it --privileged -p 6006:6006 --mount type=bind,src=C:\full\path\to\this\repo,dst=/tensorflow/models/research/custom_model detect-tutorial``

### Label images with labelImg
Label, then copy everythin in this repos images folder.

### Create tf_records
From within the Docker container in the directory ``/tensorflow/models/research/custom_model`` run: ``python generate_tfrecord.py``

TF_records should be created.

### Train the model
in the same dir run: 
``python train.py --logtostderr --train_dir=train/ --pipeline_config_path=model/custom_pipeline.config``
alternatively try:
``python model_main.py --logtostderr --train_dir=train/ --pipeline_config_path=model/cusom_pipeline.config``


