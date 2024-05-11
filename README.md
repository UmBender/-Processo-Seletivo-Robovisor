# Prova de conceito
Aqui está o projeto implementado em Python para a prova de conceito proposta no desafio seletivo. 
Para atender às demandas das especificações definidas, foram criados dois processos.
Um deles é responsável por salvar em um arquivo o texto recebido através dos posts enviados pelo cliente assinante. 
O outro processo instanciado será responsável por executar o festival.
O diagrama da arquitetura do projeto.


## Diagrama
![alt text](./Diagrama.png)

## Especificações
No projeto foi utilizado as bibliotecas paho-mqtt e asyncio.
O projeto foi configurado hardcode, pois se trata de uma prova de conceito.
A porta utilizada será a 1883, e os post serão no tópico test/status.
