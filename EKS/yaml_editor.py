###
# Código usado para gerar TAML para EKS
# Autoria de Carlos Dip
###

###
# Code used for EKS YAML automation
# Made by Carlos Dip
###

import yaml

def build_exp_list(n):
    output = []
    for i in range(n):
        output.append({'name': f'experiment-{i}', 
        'image': 'public.ecr.aws/q1b7b4u6/cedipengineering/docker_ml_ecr:latest', 
        'ports': [{'containerPort': 80}], 
        'env': [{'name': 'MLFLOW_TRACKING_URI', 
                'value': 'http://3.143.228.222:5000'}, 
                {'name': 'experiment_name', 
                'value': f'mlflow_measurement_eks_{n}_exp'}, 
                {'name': 'layersTypes', 
                'value': 'Dense Dropout Dense Dropout Dense'}, 
                {'name': 'layersSizes', 
                'value': '64 0.5 64 0.5 1'}, 
                {'name': 'layersActivations', 
                'value': 'relu None relu None sigmoid'}, 
                {'name': 'epochs', 
                'value': '3'}, 
                {'name': 'batch_size', 
                'value': '128'}, 
                {'name': 'master_ip', 
                'value': 'http://3.143.228.222:5000'}], 
        'command': ['python3'], 
        'args': ['./docker_exec_file/runner.py']})
    return output
base = ""
with open("main_deploy_base.yaml",'r') as doc:
    base = yaml.load(doc, yaml.FullLoader)
    
for i in [12, 16, 24, 32, 48, 64, 100]:
    exps = build_exp_list(i)
    base["metadata"]["namespace"] = f"docker-exp-{i}"
    base["spec"]["template"]["spec"]["containers"] = exps[:]
    with open(f"main_deploy_{i}.yaml", "w") as doc:
        yaml.dump(base, doc, sort_keys=False)
