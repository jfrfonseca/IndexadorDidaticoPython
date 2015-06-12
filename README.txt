##############################################################################
##############################################################################
###																		   ###
###			 /==========================\     ++++++++++++++++++++++++	   ###
###			<== INDEXADOR SIMPLIFICADO ===>   Version 3.15.6.01.9 Ind5	   ###
###			 \==========================/	  ++++++++++++++++++++++++	   ###
###																		   ###
###		José F. R. Fonseca, Graduando				License: MIT, 2015	   ###
###		jfra.fonseca@gmail.com											   ###
###		Pontifícia Universidade Católica de Minas Gerais, Brasil		   ###
###																		   ###
###		O sistema descrito por este documento age como um Indexador e	   ###
###		processador de pesquisas booleanas de documentos da base de dados  ###
###		corpus1g, disponibilizados previamente. Feito como parte dos	   ###
###		requisitos para a conclusão da disciplina Tópicos Especiais em	   ###
###		Informática II - Recuperação de Informação, do curso de 		   ###
###		barcharelado em Ciência da Computação da PUC Minas em Belo         ###
###		Horizonte, Brasil.												   ###
###																		   ###
##############################################################################
##############################################################################

 /==============\
=== UTILIZAÇÃO ===============================================================
 \==============/

1. QUERY
	Navegue até o diretório com os arquivos do programa
	Execute a linha de comando:

-------------------------------
python processQueries.py $QUERY
_______________________________

	sendo $QUERY uma string típica, do padrão:
$QUERY = termo [(AND|OR) termo]*
	@ ATENÇÃO!! ESTE PROGRAMA REALIZA QUERIES DISJUNTIVAS!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. INDEXAÇÂO - ADIÇÂO DE ARQUIVOS
	Para adicionar mais arquivos à um índice existente, abra o arquivo
"makeInvertedIndex.py" e modifique as linhas com os valores para:

-------------------------------------------------------------------------------
DATABASE_ITEM = "NOME"  # valor do nome do arquivo de database/nome da database
DATABASE_FILE = "diretório_da_database"+DATABASE_ITEM  # diretório da database,
seguido do nome da mesma
DATABASE_INDEX_FILE = "indice_da_database"  # arquivo de índice da database,
no mesmo formato dos arquivos de índice da database corpus1g
_______________________________________________________________________________

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3. INDEXAÇÂO - CRIAÇÃO DE NOVO ÍNDICE
Localize no arquivo "makeInvertedIndex.py" a linha abaixo, e modifique-a para
o nome desejado do novo arquivo de índice.
GENERATED_INVERTED_INDEX = "nome_do_indice"
Depois, crie os arquivos de nome "metaIndex-nome_do_indice.dat" e
"namesDict-nome_do_indice.dat", cujo conteúdo deve ser apenas um casal de
colchetes:
{}
Por fim, após navegar até a página dos códigos, execute a linha de comandos:
 
----------------------------
python makeInvertedIndex.py
____________________________

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. BASES COMPACTADAS - FLATTEN
Localize no arquivo "parseDocument.py" a linha abaixo, e troque seu valor para
"True", caso a base de dados esteja compactada com o algoritmo Flatten.

------------------
COMPRESSED = False
__________________


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 /================\
=== DOCUMENTAÇÃO =============================================================
 \================/
Esta documentação apresenta descrições gerais sobre o programa INDEXADOR
SIMPLIFICADO, em sua versão 3.15.5.31.7 Ind3. Estas descrições abrangem
funcionalidades e análises, sendo que mais detalhes podem ser encontrados
nos arquivos de implementação, também descritos nesta documentação.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. SOBRE ESTE PROGRAMA
Esta documentação, e o código que a mesma acompanham, implementam ou descrevem
 as funções descritas abaixo, na forma descrita abaixo, de acordo com as
convenções PEP-8. Entre outras normas, estas convenções definem que arquivos
não devem ter mais de 79 caracteres por linha, regra aplicada mesmo à esta
documentação. Quando, por algum motivo, a norma teve de ser desrespeitada, foi
 incluido um comentário ao fim da linha, "  # @IgnorePep8".
Um indexador de arquivos adapta os mesmos para uma estrutura eficiente para
pesquisas por termos, um índice, que relaciona termos e documentos que os
contém. Este programa lê a base de dados provida, gera uma estrutura
denominada Indice Invertido, e processa consultas feitas à tal base de dados.

	1.1 Base de Dados Corpus1g
A base de dados utilizada neste programa é chamada "corpus1g", e contém 5.7Gb
de dados de páginas HTML, PHP, documentos DOC, vídeos SFW, entre outros tipos
de documentos típicos do ambiênte de rede WEB. A base de dados está dividia em
4 arquivos - pagesRI0 a 3, contenedores dos documentos, e também contém um
indice próprio, que identifica o nome posição de cada documento dentro dos
arquivos como offset de bytes de seu começo.  

	1.1 Índice Invertido
Um índice invertido é uma estrutura de dados que acelera o processo de busca
nos dados indexados, tendo em cada linha um termo, e para cada termo uma lista
ordenada com elementos representando cada arquivo indexado da base que contém
tal termo. Dentro de cada elemento, ainda há uma sub-lista que informa as
posições de cada ocorrência do termo no documento.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2. DECISÕES GERAIS SOBRE A IMPLEMENTAÇÂO
Este programa foi implementado na linguagem Python de programação.De propósito
geral, esta linguagem é indicada para problemas de tratamento, busca,
normalização e análize de dados, em contextos onde a portabilidade e
facilidade de implementação e análise são preferidos sobre eficiência e
controle preciso da plataforma de execução. A linguagem Python, em sua versão
2.7.6, possui, embutida, todo tipo de bibliotecas para tratamento de dados.
Devidas as suas características didáticas, esta linguagem foi considerada
ideal para este trabalho acadêmico.
Foi determinado que não fossem incluídas bibliotecas novas, tendo sido
utilizadas apenas as bibliotecas nativas da versão 2.7.6 da linguagem Python.

	2.1 Python
A linguagem Python, de propósito geral, utiliza pesadamente o conceito de
orientação à objetos, e os preceitos Unix de "tudo são arquivos". Muito de
sua filosofia se assemelha à programação em scripts de sistema, sendo bastante
 similar à linguagem Perl, muito mais antiga. Contudo, Python "formaliza" Perl,
eliminando expressões regulares na implementação, e colocando grande ênfase na
 identação do código, que faz por veses o papel de caracteres de escopo em
linguágens como Java.
Python é uma linguagem interpretada-compilada, normalmente implementada em C
ou Java, e portanto muito portátil. Ainda assim, é considerada uma linguagem
de Scripting, altamente legível e de fácil implemtação.
Python baseia-se muito na noção de "Listas Abstratas", coleções ordenadas de
objetos, que podem ser acessadas em qualquer ordem, concorrente e
eficientemente. Python abstrai acessos e funções atômicas, muitas veses
extraindo paralelismo implícito. Outra utilidade da linguagem é a abstração e
inclusão de de funções-lambda implícitas, que podem estar inlcuidas diretamente
 dentro da definição de listas, fazendo um tratamento para certos elementos da
lista, como sintaxe:
lista_com_tratamento = [tratamento_função_X(elemento) for elemento in
							lista_sem_tratamento if
								condições_selecionando_elementos]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3. MÓDULOS
Na linguagem Python, de alto-nível, arquivos de código distintos são
denominados "módulos", seguindo uma filosofia de orientação à objetos. Os
módulos de código fonte tem extensão ".py", e podem ser "compilados" como
".pyc" pelo sistema operacional como otimização, o que não é necessário para
seu funcionamento.
Este programa implementa quatro módulos, que devem ser posicionados no mesmo
diretório: processQueries.py, makeInvertedIndex.py, fileIO.py, e
parseDocument.py. Os documentos estão relacionados da forma a seguir, sendo
que o símbolo "+2" dentro dos colchetes à frente de um documento indica que o
mesmo possui duas dependências, o valor 0 que o documento não possui
dependências, o símbolo "@" que o documento é executável, o caractere "O" para
documentos que definem objetos.
Um documento reprezentado logo abaixo e identado mais à direita abaixo de
outro representa uma de suas dependências.

[0, @] processQueries.py		[+2, @] makeInvertedIndex.py
									[0, O]--- parseDocument.py
									[0, O]--- fileIO.py

	3.1 processQueries.py
Este documento realiza todas as operações de processamento de queries, e pode
ser executado por meio da linha de comando:
python processQueries.py QUERY
A "QUERY" fornecida deve seguir o padrão:
termo1 [(AND|OR) termo2]*

	3.2 makeInvertedIndex.py
Este módulo realiza a indexação da base de dados setada em uma variável do
mesmo. Pode ser chamado diretamente pela linha de comandos, não necessitando
de argumentos ou parâmetros para ser executado. Depende de parseDocuement.py,
e fileIO.py.

	3.3 parseDocument.py
Este módulo não pode ser executado independentemente. Reune as funções e
objetos privados que realizam o parse de um documento, especificada sua
localização. Define e instancia uma classe, local e provada.

	3.4 fileIO.py
Este módulo lida com o controle de acesso ao disco, por meio de um objeto
público definido nesta classe. Escreve e lê dados do disco, e mantem um
controle de modificações. Computacionalmente leve, ainda é o módulo de maior
tempo, pois contém as ações mais temporalmente significativas.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. ARQUIVOS
Diversos arquivos são necessários para o funcionamento correto deste programa.
Estes arquivos devem estar disponíveis na mesma pasta que os códigos. São eles:

	4.1 __init__.py
Arquivo vazio, necessário para o funcionamento do código em Python.

	4.2 invertedIndex.dat
Arquivo que contém o índice invertido, logo, o arquivo com os dados principais
deste programa. Tambem o maior arquivo, em quantidades de bytes.

	4.3 metaIndex-invertedIndex.dat
Meta-arquivo que contém o dicionário de tradução de termos para hash, para
otimização do acesso ao índice invertido.

	4.4 namesDict-invertedIndex.dat
Meta-arquivo que contém um dicionário relacionando nomes de arquivos com seus
respectivos hashes, para otimizar o acesso ao disco.

	4.5 Backup_"seconds_since_epoch"_invertedIndex.dat
Um arquivo de backup do índice tal qual no momento determinado, que mede a
quantidade de segundos desde Epoch (00:00:00 de 01/01/1980, Greenwitch)

5. RUNTIME
O programa pode demorar várias horas para indexar uma base de dados de tamanho
considerável, contendo milháres de documentos, mas apenas alguns segundos para
realizar uma busca no índice de tal base.

6. COMPLEXIDADE
Por meio da ferramenta cProfile, e a linha de código abaixo, é possível
identificar o perfil de execução do código, ordenada pelo tempo de execução
total de uma determinada função, desconsiderando-se o tempo gasto em
sub-chamadas. Pode se ver que as funções mais custosas são as que envolvem
acessos ao disco, de leitura ou escrita. 

--------------------------------------------------
python -m cProfile -s tottime makeInvertedIndex.py
__________________________________________________

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

