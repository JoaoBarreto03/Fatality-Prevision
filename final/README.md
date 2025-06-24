# Previsão de Fatalidades em Desastres Naturais

Projeto da disciplina de Aprendizado de Máquina (Mini Trabalho 8) – UnB/FCT/Engenharia

## Equipe

- Caio Felipe Alves Braga - 211030694
- Guilherme Evangelista Ferreira dos Santos - 200038028
- Isabelle da Costa Figueiredo - 211039500
- João Manoel Barreto Neto - 211039519
- Leonardo Gonçalves Machado - 211029405
- Mylena Angélica Silva Farias - 211029497

---

## Objetivo

Desenvolver um sistema preditivo para estimar o número de fatalidades em desastres naturais, utilizando dados históricos e variáveis socioeconômicas, visando apoiar decisões em gestão de riscos e resposta a emergências.

---

## Bases de Dados

- **EM-DAT**: Eventos e fatalidades de desastres naturais.
- **World Bank**: PIB per capita.
- **UNDP**: Índice de Desenvolvimento Humano (IDH).
- **GHSL**: Densidade populacional e distribuição urbana.

---

## Arquitetura e Ambiente

- **Ambiente**: Python 3.10+, bibliotecas: numpy, pandas, scikit-learn, scipy.
- **Estrutura**: Pipeline modular (pré-processamento, modelagem, avaliação).
- **Automação**: Scripts Python, versionamento Git.
- **Fluxo**:
  1. Carregamento e integração dos dados.
  2. Engenharia de atributos (ex: interação PIB x IDH).
  3. Winsorização e padronização.
  4. Treinamento de modelos (Random Forest, Gradient Boosting, ensemble).
  5. Avaliação e geração de predições.

---

## Execução

```python
import pandas as pd
from modelo import treinar_e_avaliar_modelos

df = pd.read_excel('base_com_hdr_e_gdp.xlsx')
resultados = treinar_e_avaliar_modelos(df)
print(resultados)
```

## Testes

- Validação cruzada (KFold) para robustez.
- Testes de desempenho (MAE, RMSE, R²).
- Testes com dados reais e simulados.

---

## Bases de Dados

- **EM-DAT**: Eventos e fatalidades de desastres naturais.
- **World Bank**: PIB per capita.
- **UNDP**: Índice de Desenvolvimento Humano (IDH).
- **GHSL**: Densidade populacional e distribuição urbana.

---


## Arquitetura e Ambiente

- **Ambiente**: Python 3.10+, bibliotecas: numpy, pandas, scikit-learn, scipy.
- **Estrutura**: Pipeline modular (pré-processamento, modelagem, avaliação).
- **Automação**: Scripts Python, versionamento Git.
- **Fluxo**:
  1. Carregamento e integração dos dados.
  2. Engenharia de atributos (ex: interação PIB x IDH).
  3. Winsorização e padronização.
  4. Treinamento de modelos (Random Forest, Gradient Boosting, ensemble).
  5. Avaliação e geração de predições.

---


## Empacotamento e Deploy

- Organização em pastas: `/src`, `/data`, `/notebooks`, `/tests`.
- Dependências especificadas em `requirements.txt`.
- Deploy recomendado via ambiente virtual ou Docker.

### Instalação

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Versão Inicial

- **v1.0.0**: Pipeline completo, aceita dados EM-DAT + variáveis externas, retorna predição de fatalidades.
- **Limitações**: Não cobre todos os tipos de desastre, depende da qualidade dos dados externos.
- **Resultados**: MAE e RMSE validados em conjunto de teste real.

---

## Monitoramento

- **Indicadores**: MAE, RMSE, tempo de resposta, taxa de erro de entrada, número de predições/dia.
- **Ferramentas**: Logs estruturados, Prometheus, Grafana, scripts de verificação automática, alertas por e-mail.
- **Frequências**: Métricas em tempo real, análises quinzenais/mensais, atualização anual das bases externas.

---

## Manutenção e Atualização

- Atualização anual das bases externas.
- Revalidação semestral do modelo.
- Controle de versão com Git e CHANGELOG.md.
- Processo de rollback em caso de regressão.

---

## Exemplo de execução

Veja exemplos de execução e resultados no [notebook do projeto](https://colab.research.google.com/drive/1uu6xEDh3iMkeyktb6D9WG4GoOFbg_fcN?usp=sharing#scrollTo=LamNB2hK5h8b).

---

## Referências

- [EM-DAT](https://www.emdat.be)
- [World Bank](https://data.worldbank.org)
- [UNDP](https://hdr.undp.org)
- [GHSL](https://ghsl.jrc.ec.europa.eu)
- Hastie, Tibshirani, Friedman. The Elements of Statistical Learning.
- Russell, Norvig. Artificial Intelligence: A Modern Approach.