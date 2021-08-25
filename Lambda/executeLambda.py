###
# Código usado para executar Lambda
# Baseado numa resposta do Stack Overflow (https://stackoverflow.com/questions/54880339/multiple-parallel-aws-lambda-invocations)
# Autoria de Carlos Dip
###

###
# Code used to execute Lambda
# Based on answer from Stack Overflow (https://stackoverflow.com/questions/54880339/multiple-parallel-aws-lambda-invocations)
# Made by Carlos Dip
###

import time
import json
import asyncio
import aiobotocore

async def invoke(payload, session):
    async with session.create_client('lambda', region_name='us-east-2') as client:
        return await client.invoke(FunctionName='arn:aws:lambda:us-east-2:461597312227:function:example', Payload=payload)

def ker_lay_str(lType: str, depth: int,  input_dim: int = None, activation: str = "relu"):
    if lType == "Dropout":
        return [lType, depth]
    if input_dim is not None:
        return [lType, depth, activation, input_dim]
    return [lType, depth, activation]

def generate_invocations(payloads, session):
    for payload in payloads:
        yield invoke(payload, session)

def invoke_all(payloads):
    loop = asyncio.get_event_loop()

    async def wrapped():
        session = aiobotocore.get_session()
        invocations = generate_invocations(payloads, session)
        return await asyncio.gather(*invocations)

    return loop.run_until_complete(wrapped())

# Execução:
def main():
    
    
    
    for exp_count in [4,8,12,16,24,32,48,64]:
        payloads_list = []  # MY PAYLOADS LIST    
        # Variáveis compartilhadas por todos os experimentos (É possível configurá-los individualmente, mas isso facilita)
        master_ip = "http://3.143.228.222:5000/"
        experiment_name = f"mlflow_measurement_lambda_{exp_count}_exp"
        # Adição de experimentos à lista. Caso deseje usar um tipo de layer ou função de ativação diferente, 
        # verifique que ker_lay_str() é capaz de converter isso, e que o código do Lambda é capaz de parsear isso de volta. 
        for i in range(exp_count):
            # Bloco para copiar e colar para adicionar novos experimentos:
            payloads_list.append(bytes(json.dumps(
                {"layers":[ker_lay_str("Dense", 64, 20, "relu"), 
                        ker_lay_str("Dropout", 0.5), 
                        ker_lay_str("Dense", 64, "relu"), 
                        ker_lay_str("Dropout", 0.5), 
                        ker_lay_str("Dense", 1, "sigmoid")],
                "epochs":3,
                "batch_size":128,
                "experiment_name":experiment_name,
                "master_ip": master_ip}
            ), encoding='utf8')) 
            # // ------------------------------------------------ //
        # Começa todas as invocações e cronometra o tempo total.
        start = time.perf_counter()
        lambda_responses = invoke_all(payloads_list)
        # print(lambda_responses)
        print(f"Tempo total de execução: {time.perf_counter()-start}\nNúmero de execuções: {len(payloads_list)}")
        print("Agora esperando 10 min")
        time.sleep(60*10)

if __name__ == '__main__':
    main()