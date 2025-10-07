# 🚢 Titanic Survival Simulator — MLET_FASE3_TC

> Projeto do Tech Challenge (FIAP) com **ingestão de dados**, **treinamento de modelos de ML** e **API FastAPI** com interface para simulação de sobrevivência no Titanic.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg?logo=fastapi&logoColor=white)](#)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E.svg?logo=scikitlearn&logoColor=white)](#)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#)

---

## 📸 Demo rápida

- Abra a app e clique em **“Gerar Passageiro”** para ver a predição (rótulo e probabilidade).
- Interface: `templates/simulator.html`
- Backend: `predict_app.py` → **`GET /`** (página) e **`GET /simulate`** (predição aleatória).

> Dica: inclua aqui um GIF/print da tela quando publicar o vídeo.

---

## 🧭 Arquitetura (resumo)

```
Kaggle → API de Ingestão (FastAPI) → SQLite/CSV
                          │
                          ├── Notebooks de treino (Logística, Árvore)
                          │       └── Artefatos: modelo/*.pkl
                          │
                App de Predição (FastAPI) → UI (Jinja/Bootstrap)
```

- **API de Ingestão** (`API/main.py`): baixa o dataset do Kaggle e cria `FASE3_TC/data/PROCESSED/titanic.db` no startup.
- **Treino** (`modelo.ipynb` / `DecisionTree_Titanic.ipynb`): prepara dados, treina e salva `.pkl`.
- **Serving** (`predict_app.py`): carrega `modelo/modelo_final.pkl` e serve a UI/endpoint.

---

## 🧰 Stack

- **Python** 3.10+
- **FastAPI** + **Uvicorn**
- **Jinja2** (templates HTML/Bootstrap)
- **pandas**, **numpy**
- **scikit-learn** (Regressão Logística, Árvore de Decisão)
- **joblib** (serialização do modelo)
- **Kaggle API** (ingestão de dados)

---

## 🚀 Como rodar

> Exemplos para Windows (PowerShell). Em macOS/Linux, adapte a ativação da venv.

1) **Clonar & entrar**
```bash
git clone https://github.com/<user>/MLET_FASE3_TC.git
cd MLET_FASE3_TC
```

2) **Ambiente & dependências**
```powershell
py -3.11 -m venv .venv         # ou py -3.12
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# se faltar algo:
pip install scikit-learn numpy pandas joblib uvicorn[standard] fastapi jinja2
```

3) **(Opcional) Ingestão do Kaggle → SQLite**
```powershell
# Credenciais Kaggle (NÃO versionar):
#   Windows: %USERPROFILE%\.kaggle\kaggle.json
#   Linux/Mac: ~/.kaggle/kaggle.json
# Ou defina KAGGLE_CONFIG_DIR apontando para a pasta com kaggle.json
python -m uvicorn API.main:app --reload
# No startup, a API baixa o CSV (se necessário) e cria FASE3_TC/data/PROCESSED/titanic.db
```

4) **App de predição**
```powershell
python -m uvicorn predict_app:app --reload
# abrir: http://127.0.0.1:8000/
```

> **Importante:** o arquivo **`modelo/modelo_final.pkl`** precisa existir.  
> Se não existir, treine e salve (ver seção “Treinando modelos”).

---

## 📦 Estrutura

```
API/
  └── main.py                     # Ingestão Kaggle → CSV/SQLite (startup)
modelo/
  └── modelo_final.pkl            # Artefato carregado pelo app (vencedor)
templates/
  └── simulator.html              # UI (Bootstrap) com botão "Gerar Passageiro"
predict_app.py                    # FastAPI (/, /simulate)
DecisionTree_Titanic.ipynb        # Notebook Árvore de Decisão
modelo.ipynb                      # Notebook Logística (Erick)
requirements.txt
```

---

## 🧪 Features usadas (ordem **exata**)

```
[Pclass, Age, SibSp, Parch, Fare, Sex_male, Embarked_C, Embarked_Q, Embarked_S]
```

- **Pclass** (1–3), **Age**, **SibSp**, **Parch**, **Fare**
- **Sex_male**: 1 = masculino, 0 = feminino
- **Embarked_C/Q/S**: dummies do porto de embarque (C, Q, S)

> A mesma ordem/quantidade **deve** ser mantida no treino e na predição.

---

## 📊 Treinando modelos

### 1) Regressão Logística (notebook do Erick)
- Pré-processa (dummies) e treina `LogisticRegression`.
- Salva artefato: `modelo/modelo_final.pkl` (usado pelo app).

### 2) Árvore de Decisão
- Notebook: **`DecisionTree_Titanic.ipynb`**  
- Passos: carregar dados (CSV/SQLite) → imputar (mediana/moda) → criar dummies `Sex_male` + `Embarked_*` → **baseline** e **tuning (GridSearchCV)** → métricas (ROC AUC, Accuracy, Precision, Recall, F1), **curva ROC**, **matriz de confusão** → salvar artefatos:
  ```
  modelo/modelo_arvore.pkl
  outputs/metrics_tree.json
  ```
- Para usar a árvore no app: substitua `modelo_final.pkl` pelo artefato desejado:
  ```powershell
  copy modelo\modelo_arvore.pkl modelo\modelo_final.pkl
  ```

### 3) Comparação (sugestão)
Compare **Logística × Árvore** no **mesmo split** e com as **mesmas features** — métrica principal **ROC AUC**, secundárias **F1/Recall**.  
(Adicione um script/nb de comparação e salve um `outputs/compare_log_vs_tree.json`.)

---

## 🌐 Endpoints

- **GET /** → renderiza `simulator.html`
- **GET /simulate** → gera um passageiro aleatório e retorna:
  ```json
  { "survived": true/false, "probability": 0.743, "passenger_profile": { ... } }
  ```
- **(Planejado)** `POST /predict` com payload manual (formulário) — ainda não implementado.

---

## 🧪 Métricas (exemplo — substitua pelos seus números)

| Modelo                 | ROC AUC | Accuracy | Precision | Recall | F1   |
|------------------------|:------:|:--------:|:---------:|:------:|:----:|
| Regressão Logística    |  0.80  |   0.81   |   0.76    |  0.74  | 0.75 |
| Árvore de Decisão (bl) |  0.78  |   0.79   |   0.74    |  0.71  | 0.73 |

- **Curvas ROC** e **Matriz de Confusão**: ver plots nos notebooks / `outputs/`.
- Política de decisão (threshold): padrão **0.50**.  
  (Opcional: otimizar threshold por **F1** em validação e apenas **reportar** no teste.)

---

## 🔒 Boas práticas & avisos

- **Nunca** versione `kaggle.json` (credenciais).
- `.pkl` executa código quando carregado → **não** carregue artefatos de fontes desconhecidas.
- Fixe **`random_state`** para reprodutibilidade.
- Mantenha `requirements.txt` atualizado (inclua `scikit-learn`).

---

## 🛠️ Troubleshooting

- **`uvicorn: command not found`**  
  `pip install uvicorn[standard]` e rode `python -m uvicorn predict_app:app --reload`.

- **`ModuleNotFoundError: sklearn` (ao carregar .pkl)**  
  `pip install scikit-learn` (o artefato depende dela).

- **`X has 8 features, model expects 9`**  
  Alinhamento de features. Garanta exatamente:
  ```
  [Pclass, Age, SibSp, Parch, Fare, Sex_male, Embarked_C, Embarked_Q, Embarked_S]
  ```

- **Kaggle não autentica**  
  Coloque `kaggle.json` em %USERPROFILE%\.kaggle\ (Win) ou ~/.kaggle/ (Linux/Mac); ou defina KAGGLE_CONFIG_DIR.

---

## 🗺️ Roadmap

- [ ] Adicionar **POST /predict** + formulário na UI  
- [ ] Comparar com **RandomForest / Gradient Boosting**  
- [ ] **Calibrar probabilidades** e **ajustar threshold** por objetivo  
- [ ] Métricas por subgrupos (ex.: `Sex`, `Pclass`)  
- [ ] Dockerfile para execução containerizada

---

## 👥 Autores

- **Pedro** — Business Intelligence / Engenheiro  
- **Erick** — Modelagem inicial (Regressão Logística) & repositório original

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Sinta-se livre para usar, adaptar e contribuir.

---

> Dúvidas ou sugestões? Abra uma issue ou PR. Bons estudos e bora afundar menos modelos! 🛟
