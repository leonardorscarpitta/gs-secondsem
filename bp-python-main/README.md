# Python - GS

## Descrição do projeto
Este projeto tem como objetivo abordar a crescente necessidade de soluções acessíveis de energias renováveis, com foco especial em comunidades e regiões mais carentes. A iniciativa utiliza python para conexão a dispositivos e o monitoramento de dados relacionados ao desempenho na coleta e no armazenamento de energia solar.

Essa abordagem não apenas explora soluções tecnológicas inovadoras, mas também contribui para a democratização do acesso à energia sustentável em locais onde a infraestrutura convencional é limitada.

## Dependencias
- [Python](https://www.python.org/); <br>
- Bibliotecas necessárias: requests & matplotlib <br>
    - Utilize `pip install requirements.txt` quando estiver no diretório do programa;

## Manual de execução
1. Navegue até um destino de preferência do seu computador utilizando a linha de comando `cd desktop`; <br>
2. Clone o projeto GitHub utilizando o comando `git clone https://github.com/Bright-Path-Team/bp-python.git`; <br>
3. Navegue até o projeto: `cd bp-python`; <br>
4. Crie um arquivo `.env` para configurar o IP da máquina da seguinte forma (como uma variável de ambiente): <br>
    ```
    ip="IP-da-maquina"
    ```
5. Certifique-se de que você tem todas as [dependências necessária](https://github.com/Bright-Path-Team/bp-python?tab=readme-ov-file#dependencias); <br>
6. Caso utilize **Linux** ou **Mac**, altere na linha `10`, o `"cls"` para `"clear"` para evitar erros de execução do programa;

## Requisitos do sistema

### Requisitos Funcionais (RF)
1. Verificação de Conexão ao Servidor <br>
1.1 O sistema deve verificar a conexão com o servidor no endereço IP configurado em um arquivo .env. <br>
2. Interatividade com o Usuário via Menu <br>
2.1 Deve apresentar um menu interativo com as seguintes opções: <br>
3. Monitoramento da placa leste. <br>
3.1 Monitoramento da placa oeste. <br>
3.2 Monitoramento da eficiência energética. <br>
3.3 Salvar dados coletados em um arquivo JSON. <br>
3.4 Gerar gráficos de monitoramento. <br>
3.5 Encerrar o programa. <br>
4. Coleta de Dados de Monitoramento <br>
4.1 O sistema deve realizar requisições a um servidor para obter os valores de:
- Desempenho da placa solar leste.
- Desempenho da placa solar oeste.
- Eficiência energética média das placas. <br>
5. Armazenamento de Dados <br>
5.1 O sistema deve salvar os dados coletados em um arquivo JSON, com o formato adequado para posterior análise. <br>
6. Geração de Gráficos <br>
6.1 O sistema deve gerar gráficos dos dados coletados (placa leste, placa oeste e eficiência energética) em função do tempo. <br>
7. Mecanismo de Reconexão <br>
7.1 Caso a conexão com o servidor falhe, o sistema deve tentar reconectar automaticamente após um temporizador configurável. <br>
8 Mensagens de Feedback <br>
8.1 Deve exibir mensagens claras para o usuário indicando status, como sucesso na conexão, erros ou progresso das operações. <br>
9. Encerramento do Programa <br>
9.1 O programa deve permitir ao usuário finalizar a execução de forma segura, exibindo uma mensagem de encerramento.

### Requisitos Não Funcionais (RNF)
1. Interface de Linha de Comando (CLI) <br>
1.1 O sistema deve operar em um ambiente de linha de comando, com mensagens formatadas para facilitar a leitura. <br>
2. Configuração via Variáveis de Ambiente <br>
2.1 O endereço IP do servidor deve ser configurado em um arquivo .env. <br>
3. Desempenho <br>
3.1 O tempo de resposta para verificar a conexão com o servidor deve ser adequado, com um timeout configurável. <br>
3.2 Gráficos devem ser gerados em menos de 5 segundos para conjuntos de dados típicos. <br>
4.Manutenção e Extensibilidade <br>
4.1 O código deve ser modular, com funções reutilizáveis para operações como requisições, exibição de mensagens e manipulação de dados. <br>
4.2 O sistema deve suportar expansão futura, como monitoramento de novas variáveis. <br>
5. Compatibilidade <br>
5.1 Deve ser compatível com sistemas operacionais Windows, Linux e Mac, com a possibilidade de configurar o comando de limpeza (cls ou clear). <br>
6. Segurança <br>
6.1 O sistema não utiliza nenhum tipo de conexão com outros servidores além do servidor que estão sendo feitas as requisições, isto é, não coleta nenhum dado do usuário. <br>
7. Conformidade com Padrões <br>
7.1 O JSON gerado deve seguir o padrão ISO para timestamps. <br>
7.2 As mensagens devem usar códigos ANSI para realce de texto, garantindo a leitura em terminais compatíveis. <br>
8. Dependências e Instalação <br>
8.1 O sistema deve depender apenas de bibliotecas amplamente suportadas e de fácil instalação via pip (requests, dotenv, matplotlib).

## Desenvolvedores do projeto:

| **Nome** | **RM**                 | **LinkedIn** |
|--------------------------------|------------------------|----------|
| Murilo Justi                   | RM 554512              | <a target="_blank" href="https://www.linkedin.com/in/murilo-justi-rodrigues-b336b22b7/"><img src="https://media.licdn.com/dms/image/v2/D4D03AQGnXBOl96aCtQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1709252884484?e=1733961600&v=beta&t=_W2l37rEiTdk8HSG-GUrS4R_V6KddfAGj13CbkA_k0g" width="80"></a> |
| Renan Dias Utida               | RM 558540              | <a target="_blank" href="https://www.linkedin.com/in/renan-dias-utida-1b1228225/"><img src="https://media.licdn.com/dms/image/v2/D4D03AQHZyF9WkCRtDg/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1727923002401?e=1733961600&v=beta&t=foOm4Ar-LZJK6z8mu_ypyoXfkqYesw3MAc4acpeAqpU" width="80"></a> |
| Leonardo Rocha Scarpitta       | RM 555460              | <a target="_blank" href="https://www.linkedin.com/in/leonardorscarpitta/"><img src="https://avatars.githubusercontent.com/u/161969345?s=400&u=f9bdb6fa659af646efcd0cb9fb51a321f19faabc&v=4" width="80"></a> |

## Licença

Este projeto é open source sob a **MIT License with Commons Clause**. Isso significa que você pode visualizar, modificar e compartilhar o código livremente, desde que não o utilize para fins comerciais.

Para mais detalhes, consulte o arquivo [LICENSE](./LICENSE).
