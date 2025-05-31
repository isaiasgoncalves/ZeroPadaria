# ZeroPadaria
## Um novo sistema de comensais

### O que esse projeto busca resolver?

#### Como o sistema funciona
Em uma residência para estudantes universitários, todos os dias são registradas quais refeições cada residente irá comer. 
Para isso, era utilizado uma planilha que continha uma tabela por dia da semana. Cada residente preenchia sua linha respectiva àquele dia, preenchendo as colunas `almoço, jantar, café da manhã, lanche e marmita`, sendo que as colunas `café da manhã, lanche, marmita` se referem ao dia seguinte.
Em um determinanado momento de cada manhã, um responsável coletava a quantidade de cada uma das respostas e enviava para a cozinha, que preparava as refeições.

#### Problemática
O grande problema das planilhas é que ela busca, ao mesmo tempo, ser um sistema de armazenamento de dados, e uma interface gráfica de interação com esses dados, e assim como um pato, ela não faz bem nenhuma dessas duas coisas.
Era comum a planilha conter diversos erros e inconsistências, muitas vezes acidentais ou ocasionados por mau uso. Isso atrapalhava muito a dinâmica da residência. Daí surgiu a ideia de desenvolver o ZeroPadaria.

#### A solução
O ZeroPadaria é um sistema simples desenvolvido em Python, ligado a um banco de dados PostgreSQL e com interface gráfica desenvolvida em Streamlit. Seu objetivo é simples:
+ Garantir o fácil preenchimento das refeições (comensais) por cada usuário
+ Permitir a edição fácil dos comensais
+ Oferecer uma interface clara com as refeições contadas para serem passadas para a cozinha
+ Garantir que após os comensais sejam passados para a cozinha, não seja mais possível editar os comensais daquele dia.

Projeto desenvolvido por Isaías Gouvêa Gonçalves
