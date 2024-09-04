# Algoritmo de Exclusão Mútua

Este trabalho apresenta uma implementação do algoritmo de exclusão mútua para gerenciamento de acesso à região crítica por vários processos. O algoritmo foi implementado em Python e utiliza a biblioteca `threading` para criação de threads, bem como sockets para comunicação entre os processos.

## Execução

Na raiz do repositório, execute o seguinte comando para iniciar o servidor:

```bash
python3 -m mutual_exclusion.server
```

Em seguida, em outro terminal, execute o seguinte comando para iniciar um cliente:

```bash
python3 -m mutual_exclusion.client
```

Para iniciar mais de um cliente, execute o seguinte comando:

```bash
python3 -m mutual_exclusion.multiclient --workers 5 --writes 3
```

As opções `--workers` e `--writes` são ambas opcionais e definem, respectivamente, o número de processos clientes que serão criados e o número de escritas que cada cliente fará na região crítica.


## Implementação

O algoritmo de exclusão mútua consiste em um servidor que gerencia o acesso à região crítica por vários processos clientes.

O servidor mantém uma fila de requisições de acesso à região crítica e, a cada requisição, verifica se o processo pode acessar a região crítica. O acesso é concedido se o processo for o próximo da fila e se ele não está esperando que outro processo saia da região crítica.

Essa implementação se dá em dois arquivos principais: `server.py` e `client.py`.

### `server.py`

O arquivo `server.py` contém a implementação do servidor, responsável por gerenciar o acesso à região crítica por vários processos clientes. O servidor utiliza a biblioteca `socket` para criar um socket UDP e aguardar conexões de clientes.

Para gerenciar a comunicação com diferentes processos clientes, o servidor cria uma thread para cada conexão. Cada thread é responsável por receber mensagens do cliente, processá-las e adicionar o cliente às filas de requisições de acesso e liberação da região crítica.

Assim, o programa consiste das seguintes threads:

- **Thread principal:** Responsável por iniciar o programa, invocar a thread de recepção de conexões, e aguardar (e responder) comandos da interface (imprimir a lista de pedidos atual, imprimir a lista de pedidos atendidos, ou encerrar o servidor).

- **Thread de recepção de conexões:** Responsável por aguardar novas conexões de clientes e criar uma nova thread para cada conexão.

- **Thread de cliente:** Uma para cada conexão ativa. Responsável por receber mensagens do cliente conectado, processá-las e adicionar a solicitação à fila de acesso à região crítica. Também escuta mensagens de liberação da região crítica pelo cliente e as adiciona a uma segunda fila de liberação.

- **Thread de controle de acesso:** Responsável por gerenciar o acesso à região crítica. Monitora constantemente as filas de acesso e liberação e, a cada nova solicitação de acesso, verifica se o processo pode acessar a região crítica. O acesso é concedido se o processo for o próximo da fila e se ele não está esperando que outro processo saia da região crítica.

A thread de controle de acesso alterna entre dois estados: ocioso (`IDLE`) e ocupado (`BUSY`). A thread inicia no estado ocioso e, assim que uma solicitação é atendida, passa para o estado ocupado. Nesse estado, a thread observa até que a mensagem de liberação do processo que está na região crítica apareça na fila de liberação, indicando que ele saiu da região crítica. Nesse momento, a thread volta ao estado ocioso e verifica se há novas solicitações na fila de acesso.

### `client.py`

O arquivo `client.py` contém a implementação do cliente, responsável por enviar mensagens ao servidor solicitando acesso à região crítica e liberando o acesso após a escrita.

O cliente possui apenas uma thread, que se conecta ao servidor através de um socket UDP. Em seguida, inicia-se um loop em que o cliente:

1. Envia uma mensagem ao servidor solicitando acesso à região crítica;
2. Aguarda pela resposta do servidor com a liberação do acesso; 
3. Escreve a hora atual e o ID do processo no arquivo `resultado.txt`.
4. Após a escrita, o cliente envia uma mensagem ao servidor informando que liberou o acesso à região crítica;
5. Processo fica ocioso por algum tempo, até que volte a solicitar o acesso.

O processo continua até que alcance o número de escritas no arquivo definido pelo usuário, ou até que o servidor seja encerrado.

### `multiclient.py`

Para facilitar a execução de múltiplos clientes, o arquivo `multiclient.py` cria múltiplos processos clientes simultaneamente através da biblioteca `multiprocessing`. É possível definir o número de processos clientes e o número de escritas que cada cliente fará no arquivo `resultado.txt` através das opções `--workers` e `--writes`, respectivamente.

### `util.py`

O arquivo `util.py` contém funções auxiliares utilizadas em ambos os arquivos `server.py` e `client.py`, como um enumerador contendo os tipos de mensagens que podem ser enviadas entre cliente e servidor, bem como um formatador de mensagens para o formato correto.


## Decisões de projeto

### Comunicação entre processos

Para a comunicação entre processos, pode-se escolher entre o uso de sockets TCP ou UDP. No entanto, para este trabalho, foi escolhido o uso de sockets UDP, uma vez que a comunicação entre cliente e servidor é feita através de mensagens curtas e não é necessário garantir a ordem de entrega das mensagens. O uso de conexões TCP, ainda que mais robustas, adicionam considerável _overhead_ relacionado à garantia de entrega e ordem das mensagens, o que não se faz necessário para este trabalho.

### Propagação da mensagem de liberação

A principal dificuldade na implementação foi em relação ao gerenciamento do envio e recebimento de mensagens entre os processos clientes e o servidor. Ao utilizar a função `recv` do socket, a thread em execução entra em 'modo de escuta' e aguarda até que uma mensagem seja recebida. Isso impede que a thread possa realizar outras tarefas enquanto aguarda a mensagem, o que é um problema para o servidor, que precisa gerenciar múltiplos clientes simultaneamente.

Isso gerou situações em que o servidor não conseguia processar novas solicitações de acesso à região crítica enquanto aguardava a liberação de um processo que estava na região crítica. Para solucionar este problema, foi necessário criar uma thread para cada conexão de cliente, de forma que o servidor pudesse escutar mensagens de todos os clientes simultaneamente.

Outra questão foi relacionada a notificar a thread de controle de acesso sobre a liberação da região crítica. Inicialmente, a thread de recebimento de mensagens aguardava apenas o recebimento de mensagens de solicitação, e, uma vez que o processo entrasse na região crítica, era o _coordenador_ quem aguardava pela mensagem de liberação dessa thread. No entanto, a thread de recebimento de mensagens continuava 'escutando', e a mensagem de liberação acabava sendo recebida por ela, e não pelo coordenador.

Para solucionar este problema, havia duas alternativas: 1) fazer com que a thread de esscuta parasse de aguardar novas mensagens até que este processo saísse da região crítica, com o coordenador notificando, de alguma forma, que o processo obteve acesso; ou 2) manter a thread de escuta responsável por receber todas as mensagens, inclusive as de liberação, e notificar a thread de controle de acesso sobre a liberação da região crítica.

Em obediência ao princípio da responsabilidade única, foi escolhida a segunda alternativa, de forma que a thread de controle de acesso não precisasse 'se preocupar' com a recepção de mensagens de liberação, e pudesse focar apenas no gerenciamento do acesso à região crítica. De outro modo, a thread de recebimento de mensagens seria responsável por alterar o estado do coordenador, o que não deveria ser uma responsabilidade sua.

Assim, foi decidido que uma nova fila seria criada para receber as mensagens de liberação. A thread de controle de acesso, ao conceder o acesso à região crítica, passa ao estado ocupado, e passa a verificar a fila de liberação para verificar quando pode retornar ao estado ocioso, e permitir que outros processos acessem a região crítica.

### Interface

Uma interface de linha de comando foi disponibilizada para interação com o servidor, permitindo que o usuário visualize a lista de pedidos atendidos e a lista de pedidos atuais, bem como encerre o servidor. No entanto, houve, inicialmente, uma dificuldade em relação ao funcionamento do console de saída no contexto de múltiplas threads.

Como havia outras threads imprimindo linhas no console, não era possível aguardar a entrada do usuário com a função `input`, que gerava um erro. Para solucionar esse problema, os registros de saída do servidor foram redirecionados a um arquivo de log separado, de modo que não ocupassem o console principal. A thread de interface, anteriormente uma thread invocada separadamente pela thread principal, foi movida para que se tornasse a thread principal, com a função de aguardar as conexões de novos processos sendo movida para outra thread.