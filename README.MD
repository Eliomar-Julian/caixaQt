# Caixa de mercado
Programa tipo PDV para pequenos mercados de unico caixa.
Feito em Python e Qt caixaQt é ideal para pequnos negocios.

## Instalando dependencias.
1. instale o serviço Mysql em sua maquina e configure um database vazio para receber dados.
    - basta iniciar um database vazio.
2. Tenha o python apartir da versão 3.7 devidamente configurado.
    - Instale as dependencias do python.
        - __Linux:__  ```pip3 install -r requirements.txt```
        - __Windows:__  ```pip install -r requirements.txt```
3. Configure o arquivo de inicialização __mysql-server.ini__ para configurar as opçoes de seu mysql server.
    - ```
        [Server-mysql]
        host = endereco_servidor
        user = usuário_cadastrado
        password = sua_senha_admistrador
        database = nome_do_database

        [Docs]
        repository = https://github.com/Eliomar-Julian/caixaQt
        myGithub = https://github.com/Eliomar-Julian
        ```
## tela inicial
#
#
<a href="https://imgur.com/1b1EQ6Q"><img width=480 height=360 src="https://i.imgur.com/1b1EQ6Q.png" title="source: imgur.com" /></a>

# Manual de usuário.

Com uma interface amigável e de fácil manuseio e compreensão caixaQt foi pensado para ser
usado por qualquer pessoa sem ser especialista ou ter cursos complexos de operador de caixa
basta uma leitura rápida neste mini-tutorial e já será possivel operar de maneira segura 

### passo 1.

no primeiro uso será solicitado o cadastro de um administrador padrão, esse administrador
serve para cadastrar e deletar produtos cadastrados no banco de dados. Esse administrador
poderá então adicionar e retirar novos usuários do sistema.

<a href="https://imgur.com/a3AWnh9"><img width=480 height=360 src="https://i.imgur.com/a3AWnh9.png" title="source: imgur.com" /></a>

### passo 2.

agora o proximo passo é adicionar os produtos no banco de dados, para isso vá ao menú **administrar** -> **adicionar e remover produtos**, use a senha cadastrada anteriormente para ter acesso a interface de cadastro/remoção de produtos.

<a href="https://imgur.com/f8R1wmY"><img width=480 height=360 src="https://i.imgur.com/f8R1wmY.png" title="source: imgur.com" /></a>

### passo 3.

Agora depois de ter cadastrados os seus produtos já pode utilizar o caixaQt para as suas primeiras vendas, caso tenha um leitor
de códigos basta apontar para o código do produto e o mesmo será acrescentado automáticamente a lista de compras, caso
contrário deverás digitar o código da mercadoria no campo de inserção. É comum os clientes levarem mais de um produto do
mesmo tipo para o caixa então afim de adiantar o processo de caixa é possivel usar o multiplicador **(*)** para indicar a 
quantidade de produtos do mesmo tipo.

<a href="https://imgur.com/4ikut1c"><img  width=480 height=360 src="https://i.imgur.com/4ikut1c.png" title="source: imgur.com" /></a>

Caso esteja usando usando leitor de códigos não será possivél utilizar o multiplicador diretamente, porem poderás utilizar 
o campo de busca logo abaixo, então pesquisar pelo item em questão e pressionar **TAB** para cair na lista mostrada
e usar as setas direcionais **UP**/**DOWN** até chegar ao item e pressionar **ENTER** para confirmar a seleção. O código
do item aparecerá no campo de inserção e você poderá adicionar no final o multiplicador.

<a href="https://imgur.com/TVTFMAW"><img  width=480 height=360 src="https://i.imgur.com/TVTFMAW.png" title="source: imgur.com" /></a>

### passo 4.

Após passar todos os produtos é natural passar o troco, para isso acesse o campo troco que já contará com
o total da compra, basta agora inserir o valor passado pelo cliente e ver o valor a ser devolvido.

<a href="https://imgur.com/RO5gWon"><img  width=480 height=360 src="https://i.imgur.com/RO5gWon.png" title="source: imgur.com" /></a>

### passo 5.

Agora depois de passar o troco para o seu cliente basta fechar a compra atual para deixar espaço para uma nova
venda, para isso acesse o campo finalizar e pressionar **ok** para liberar o caixa a uma nova venda.

# Após seguir os passos anteriores você está "Certificado" 😋, agora só mais uma dicas...

### Removendo itens da compra

caso algum cliente desista de um produto especifico é possivel removelo da lista de compras
para isso deixe selecionado o produto em questão usando **tab->setas** e clicando em remover,
digite nome e senha e pronto o produto já não estará mais lá e o valor será descontado do total
da venda atual.

### Mudando logo.

Mude a logo para a imagem que deseja basta ir em **administrar->mudar logotipo** e escolher a logo
de sua preferencia.

### mudar o letreiro

o letreiro serve para exibir o nome do mercado ou qualquer frase de sua prefência, para acessar
use **administrar->editar letreiro** e mude para a frase que quiser, o campo de mudança aceita
html injection sendo possivel mudar as cores e fontes através de tags html.

### encerrando o periodo de caixa

para encerrar e ver o valor total do periódo de caixa acesse **encerrar** e aparecerá uma lista com
todas a vendas finalizadas, o início do periodo do caixa e o total contido no caixa até o presente
momento. Para retirar o mantante pressione o botão **limpar caixa**, todo o montante será zerado e o 
periodo se reiniciará.

# Use andróid como leitor de código de barras
[barcode to pc](https://barcodetopc.com/)
basta baixar um cliente para o pc e o app oficial na Play Store.

# Desenvolvedores...🧑‍💻

[acesse a documentação](./DOC.MD)
