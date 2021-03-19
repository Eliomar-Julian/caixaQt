## Desenho da interface

toda a interface principal está dentro do modulo interface e classe Interface.

## Controle.

Todas as regras de negócio está dentro do módulo controller, esse modulo possui
a classe MyApp que herda da classe Interface controlando assim todos os widgets da
mesma através de seus métodos.

1. entryText.
	- responsável por capturar a entrada de texto
2. replace_.
	- automatiza o método build in **replace** para substiruir **.** por **,**.
3. enterPress.
	- captura o **enter** quando pressionado afim de pegar o texto presente no campode inserção.
4. removeItem.
	- responsável por remover um item da lista de compras em caso de desistência do produto.
5. finished_thing.
	- chama a janela de troco presente no modulo **toplevels**.
6. labelUpdate.
	- atualiza os labels de apresentação de preço total e preço atual.
7. finishVars.
	- muda os labels para 'R$ 0,00' e Zera o valor total da compra.
8. cadProdFunc.
	- chama a janela de cadastrar usuários do sistema.
9. cadProdFunc.
	- chama a janela de cadastrar produtos no banco de dados.
10. searchItens.
	- chama a janela de buscar itens quando o botão **buscar** é precionado.
11. overCashieFunc.
	- chama a janela de fechar o periodo de caixa.
12. changeLogo.
	- chama a janela de troca de logotipo.
13. changeText.
	- chama a janela de troca de letreiro rolante. OBS.: O letreiro aceita tags HTML

## reimplemented

responsavel por reimplementar botoes e capturar seus eventos.

## topleves

exibe janelas do tipo **QDialog filhas** que basicamente são todas as janelas de 
dialogo exibidas ao clicar em qualquer coisa (seja menú ou botões) na janela principal.

## crud

detem todo acesso ao banco de dados através de seus métodos

|                 MÉTODO           |     FUNÇÃO                              |
|----------------------------------|-----------------------------------------|
|insertData                        | grava os dados vindos do cadastro       |
|queryCode                         | busca o código                          |
|queryCodDynamic                   | busca dinamica do campo de buscas       |
|queryAdmin                        | busca os administradores                |
|queryAll                          | busca todos os produtos para exibir     |
|queryAndDelete                    | buscar e deletar um produto             |
|insertUser                        | insere um usuário                       |
|load_null_users                   | ver se usuarios estão vazios            |


# requerimentos para rodar

- python > 3.7
	- pyside2
