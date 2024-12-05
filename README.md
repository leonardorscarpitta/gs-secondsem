# Global Solution - Segundo Semestre

Esse projeto foi desenvolvido por mim, com o apoio do time [Bright Path](https://github.com/Bright-Path-Team), foi utilizado Python para criar um painel interativo com o IoT que foi desenvolvido em C++ e utilizando o protocolo MQTT para o envio de dados através do ESP32.

## Minha contribuição nesse projeto
- Documentação do projeto;
- Configuração do **Serviço Cloud** (para este, foi escolhido o Microsoft Azure);
- Configuração dos arquivos iniciais e seleção do **Linux** - Ubuntu LTS 20.04;
- Criação de um serviço **Daemon** para criar um dashboard que atualiza em tempo real utilizando o **FlaskAPI** do **Python** - evitando assim que o dashboard feche quando ocorrer problemas no linux ou então no próprio serviço;
- Montagem da **arquitetura do projeto** para definir como o sistema funcionaria e se comunicaria com o front end como um todo;
- Desenvolvimento do código fonte em **C++** e python para criar uma lógica de funcionamento dos componentes e comunicação com a nuvem;

[IoT](/bp-edge-main/)
[Painel interativo](/bp-python-main/)

## Licença
Este projeto é open source sob a **MIT License with Commons Clause**. Isso significa que você pode visualizar, modificar e compartilhar o código livremente, desde que não o utilize para fins comerciais.

Para mais detalhes, consulte o arquivo [LICENSE](./LICENSE).