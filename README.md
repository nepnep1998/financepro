# financepro
Controle Financeiro Pessoal - FinancePro App
# 💰 FinancePro - Sistema de Controle Financeiro Pessoal

## 📋 Sobre o Projeto

O **FinancePro** é uma aplicação web moderna e intuitiva para controle financeiro pessoal, desenvolvida em Python com Streamlit. A ferramenta permite que usuários gerenciem seus gastos de forma organizada, visualizem análises detalhadas e tomem decisões financeiras mais conscientes.

## 🚀 Funcionalidades Principais

### 📊 Dashboard Interativo
- **Métricas em Tempo Real**: Visualização rápida do total gasto, gastos do mês atual, média mensal e número de registros
- **Gráfico de Evolução Mensal**: Acompanhe seus gastos ao longo dos últimos 6 meses
- **Distribuição por Categoria**: Veja como seus gastos se distribuem entre diferentes categorias
- **Gastos Recentes**: Lista dos últimos gastos com opção de remoção individual

### 💰 Gestão de Gastos
- **Adição Simplificada**: Formulário intuitivo para registrar novos gastos
- **Categorias Detalhadas**: 8 categorias pré-definidas com descrições e dicas
- **Validação de Dados**: Sistema que previne erros na entrada de informações
- **Feedback Visual**: Animações e confirmações para melhor experiência do usuário

### 📈 Análises Avançadas
- **Gráfico de Barras**: Visualização detalhada dos gastos por categoria
- **Tabela Completa**: Lista organizada de todos os gastos registrados
- **Filtros Temporais**: Opção de visualizar gastos mensais ou totais
- **Remoção Seletiva**: Capacidade de remover gastos individualmente

### ⚙️ Configurações Personalizáveis
- **Temas de Cores**: Alternar entre diferentes esquemas de cores (Azul, Verde, Roxo, Vermelho)
- **Preferências**: Configurar notificações e backup automático
- **Exportação de Dados**: Download dos dados em formato CSV
- **Gestão de Dados**: Opção de limpar todos os dados com confirmação de segurança

## 🎯 Categorias de Gastos

O sistema inclui 8 categorias principais, cada uma com:
- **Ícone representativo**
- **Descrição detalhada**
- **Cor distintiva**
- **Dica financeira útil**

### Categorias Disponíveis:
1. **🏠 Moradia** - Aluguel, financiamento, contas de utilities
2. **🚗 Transporte** - Combustível, manutenção, transporte público
3. **🍎 Alimentação** - Supermercado, restaurantes, delivery
4. **🏥 Saúde** - Consultas, medicamentos, plano de saúde
5. **🎮 Lazer** - Entretenimento, hobbies, viagens
6. **🛒 Compras** - Roupas, eletrônicos, presentes
7. **📚 Educação** - Cursos, livros, materiais escolares
8. **💼 Outros** - Despesas diversas e emergências

## 💡 Como Usar

### 1. Primeiros Passos
- Acesse a aplicação pelo navegador
- Navegue para "💰 Adicionar Gasto" para registrar seu primeiro gasto
- Preencha: descrição, valor, categoria e data
- Clique em "Salvar Gasto" para confirmar

### 2. Acompanhamento no Dashboard
- Visualize suas métricas principais no topo da página
- Acompanhe a evolução mensal no gráfico de linha
- Analise a distribuição por categoria no gráfico de pizza
- Revise gastos recentes na lista inferior

### 3. Análises Detalhadas
- Use a página "📈 Analytics" para visões mais profundas
- Explore o gráfico de barras por categoria
- Consulte a tabela completa de gastos
- Utilize a ferramenta de remoção individual se necessário

### 4. Personalização
- Acesse "⚙️ Configurações" para ajustar preferências
- Altere o tema de cores conforme sua preferência
- Configure notificações e backup automático
- Exporte seus dados para backup externo

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação principal
- **Streamlit** - Framework para aplicações web
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Criação de gráficos interativos
- **JSON** - Armazenamento local de dados

## 📁 Estrutura de Arquivos

financepro/
├── financepro_final.py # Aplicação principal
├── dados_financepro.json # Arquivo de dados dos gastos
├── configuracoes.json # Configurações do usuário
├── app_config.dat # Configuração da aplicação
└── README.txt # Este arquivo


## 🔒 Segurança e Privacidade

- **Dados Locais**: Todas as informações ficam armazenadas localmente
- **Backup Automático**: Sistema de backup previne perda de dados
- **Confirmações**: Operações destrutivas exigem confirmação explícita
- **Validação**: Entradas de dados são validadas para garantir integridade

## 🎨 Recursos Visuais

- **Design Responsivo**: Adapta-se a diferentes tamanhos de tela
- **Animações Lottie**: Elementos visuais engaging
- **Cores Gradientes**: Interface moderna e atraente
- **Ícones Intuitivos**: Navegação fácil e compreensível

## 💡 Dicas de Uso

### Para Melhores Resultados:
1. **Registre Imediatamente**: Adicone gastos assim que ocorrem
2. **Categorize Corretamente**: Use categorias apropriadas para análises precisas
3. **Revise Semanalmente**: Acompanhe seus gastos regularmente
4. **Estabeleça Metas**: Use as análises para definir objetivos financeiros
5. **Exporte Regularmente**: Faça backup dos seus dados periodicamente

### Boas Práticas Financeiras:
- Mantenha gastos de moradia abaixo de 30% da renda
- Reserve 10-15% para lazer e entretenimento
- Crie um fundo de emergência com 3-6 meses de gastos
- Revise categorias com maiores gastos para oportunidades de economia

## 🆘 Solução de Problemas

### Problemas Comuns:

1. **Dados Não Aparecem**
   - Verifique se o arquivo `dados_financepro.json` existe
   - Recarregue a página (F5)
   - Confirme que os gastos foram salvos corretamente

2. **Erro ao Salvar Gastos**
   - Verifique se todos os campos estão preenchidos
   - Confirme que o valor é maior que zero
   - Certifique-se de que a data é válida

3. **Gráficos Não Carregam**
   - Adicione alguns gastos primeiro
   - Verifique se há gastos no período selecionado
   - Recarregue a aplicação

### Limpeza de Dados:
- Use a opção "Limpar Todos os Dados" nas configurações com cuidado
- A operação é irreversível
- Sempre exporte backup antes de limpar

## 🔄 Atualizações Futuras

Funcionalidades planejadas para versões futuras:
- [ ] Sistema de metas financeiras
- [ ] Alertas inteligentes de gastos
- [ ] Relatórios de projeção
- [ ] Educação financeira integrada
- [ ] Importação de dados de bancos
- [ ] Orçamentos por categoria
- [ ] Lembretes de contas a pagar

## 📞 Suporte

Para reportar problemas ou sugerir melhorias:
1. Verifique este arquivo README
2. Confirme que está usando a versão mais recente
3. Descreva o problema detalhadamente
4. Inclua printscreens se possível

---

**💰 FinancePro** - Tornando o controle financeiro simples, intuitivo e eficaz!

*Desenvolvido com ❤️ para ajudar você a alcançar suas metas financeiras.*
