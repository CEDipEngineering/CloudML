###
# Código usado para treinamento no Lambda
# Modelo de rede neural de exemplo de https://jhui.github.io/2018/02/11/Keras-tutorial/
# Código para extração de bibliotecas do S3 baseado em https://stackoverflow.com/questions/33569045/access-denied-using-boto3-through-aws-lambda
# Modificações de autoria de Carlos Dip
###

###
# Code used for Lambda Training
# Neural Network model taken from https://jhui.github.io/2018/02/11/Keras-tutorial/
# Code for extracting libraries from S3 based on https://stackoverflow.com/questions/33569045/access-denied-using-boto3-through-aws-lambda
# Everything else was made by Carlos Dip
###


import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
import os
import io
import zipfile
import boto3
import sys
import time

def lambda_handler(event, context):
    
    start = time.time()
    load_remote_project_archive("dip-layers-lambda", "layer_pesada.zip")
    import mlflow
    
    mlflow_experiment = event["experiment_name"]
    mlflow_master_ip = event["master_ip"]

    mlflow.set_tracking_uri(mlflow_master_ip)
    try:
        experiment_id = mlflow.create_experiment(mlflow_experiment)
    except Exception:
        experiment_id = mlflow.get_experiment_by_name(mlflow_experiment).experiment_id
    with mlflow.start_run(experiment_id=experiment_id) as run:
        
        
        layers = event["layers"]
        epochs = event["epochs"]
        batch_size = event["batch_size"]

        
        x_train = np.random.random((1000, 20))
        y_train = np.random.randint(2, size=(1000, 1))
        x_test = np.random.random((100, 20))
        y_test = np.random.randint(2, size=(100, 1))

        # Build a model
        model = Sequential()
        for i in layers:
            model.add(parse_layer(i))

        # Configure the learner
        model.compile(loss='binary_crossentropy',
                    optimizer='rmsprop',
                    metrics=['accuracy'])

        # Train
        
        model.fit(x_train, y_train,
                epochs=epochs,
                batch_size=batch_size)
        
        # Evaluate		  
        score = model.evaluate(x_test, y_test, batch_size=batch_size)
        count = 0
        for lay in layers:
            count += 1
            if len(lay) >= 3:
                mlflow.log_param(str(count) + "_" + lay[0],"Layer {0} com profundidade {1} e ativação {2}".format(lay[0], lay[1], lay[-1]))
            else: 
                mlflow.log_param(str(count) + "_" + lay[0],"Layer {0} com profundidade {1}".format(lay[0], lay[1]))
        mlflow.log_metric("ScoreX", score[0])
        mlflow.log_metric("ScoreY", score[1])
        mlflow.log_metric("TimeElapsed", time.time()-start)

    return {
        'statusCode': 200,
        'body': json.dumps("Finished"),
        'event': json.dumps(event)
    }


# (Layer Type, depth, activation, input_dim)
def parse_layer(lay):
    if lay[0] == "Dropout":
        return Dropout(lay[1])
    if lay[0] == "Dense":
        if len(lay) == 4:
            return Dense(lay[1], activation=lay[2], input_dim=lay[3])
        return Dense(lay[1], activation=lay[2])
    ## Can add more layer options

def load_remote_project_archive(remote_bucket, remote_file):
    
    # Puts the project files from S3 in /tmp and adds to path
    project_folder = '/tmp/python'
    
    if not os.path.isdir(project_folder) or True: # Coloquei or True porque quero resultados consistentes
        # The project folder doesn't exist in this cold lambda, get it from S3
        boto_session = boto3.Session()

        # Download zip file from S3
        s3 = boto_session.resource('s3')
        archive_on_s3 = s3.Object(remote_bucket, remote_file).get()

        # unzip from stream
        with io.BytesIO(archive_on_s3["Body"].read()) as zf:

            # rewind the file
            zf.seek(0)

            # Read the file as a zipfile and process the members
            with zipfile.ZipFile(zf, mode='r') as zipf:
                zipf.extractall(project_folder)

    # Add to project path
    sys.path.insert(0, project_folder)

    return True