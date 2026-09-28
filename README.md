# TalkToModel-XAI

# TalkToModel-XAI
# 🧠 TalkToModel-XAI
### Conversational Explainable Artificial Intelligence for Machine Learning Models

> **Talk to your Machine Learning model. Understand its predictions. Ask why.**

**TalkToModel-XAI** is an Explainable AI (XAI) project inspired by the research work **TalkToModel: Explaining Machine Learning Models with Interactive Natural Language Conversations**.

The project explores how users can interact with machine learning models using **natural-language questions** instead of relying only on traditional charts, feature-importance plots, or technical explanation methods.

Rather than simply asking *"What did the model predict?"*, TalkToModel-XAI aims to help users ask:

- 💬 **Why did the model make this prediction?**
- 🔍 **Which features influenced the prediction?**
- ⚖️ **What would need to change for a different prediction?**
- 📊 **How does this prediction compare with other instances?**
- 🧠 **Can I understand the model without knowing how it works internally?**

---

## ✨ Key Idea

Traditional machine-learning systems often behave like black boxes:

```text
        Input Data
            │
            ▼
    ┌─────────────────┐
    │  ML Model       │
    │  (Black Box)    │
    └────────┬────────┘
             │
             ▼
        Prediction
```

The user receives a prediction but may not understand **why** it happened.

TalkToModel-XAI introduces a conversational explanation layer:

```text
             User
              │
              │ Natural-language question
              ▼
       ┌───────────────┐
       │ Conversation  │
       │    Engine     │
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │ Explanation   │
       │   Engine      │
       └───────┬───────┘
               │
               ▼
        ┌─────────────┐
        │  ML Model   │
        └──────┬──────┘
               │
               ▼
        Explanation
               │
               ▼
             User
```

This makes model explanations more accessible through an interactive dialogue.

---

# 🎯 Objectives

The main objectives of this project are:

- Make machine-learning predictions easier to understand.
- Allow users to ask questions about model behavior using natural language.
- Bridge the gap between **machine-learning models and human understanding**.
- Explore conversational approaches to Explainable AI.
- Provide explanations without requiring users to understand complex XAI terminology.
- Investigate how explanation techniques can be combined into an interactive conversational system.

---

# 🔬 Research Background

This project is based on the ideas presented in the research paper:

> **Explaining machine learning models with interactive natural language conversations using TalkToModel**

The original TalkToModel system proposes a conversational approach to XAI consisting of three major components:

1. **Adaptive Dialogue Engine**  
   Interprets a user's natural-language question and determines what explanation is being requested.

2. **Execution / Explanation Component**  
   Executes the appropriate explanation operation on the underlying machine-learning model.

3. **Conversational Interface**  
   Presents the resulting explanation to the user through natural language.

The original research demonstrated the use of conversational explanations for understanding predictions from machine-learning models, particularly for tabular prediction tasks.

---

# 🧩 Explainable AI Techniques

TalkToModel-XAI can be viewed as a conversational layer over established XAI techniques.

### 🔹 SHAP

**SHAP (SHapley Additive exPlanations)** explains a prediction by estimating how much each feature contributes to the model's output.

Example:

```text
Prediction: High Risk

Feature             Contribution
---------------------------------
Age                    +0.32
Income                 -0.18
Credit Score           -0.27
Debt                   +0.41
```

This allows the system to answer questions such as:

> "Which features contributed most to this prediction?"

---

### 🔹 LIME

**LIME (Local Interpretable Model-agnostic Explanations)** creates a simple interpretable approximation of a complex model around a particular prediction.

It is useful for answering questions such as:

> "Why was this particular instance classified this way?"

---

### 🔹 Counterfactual Explanations

Counterfactual explanations investigate what changes to an input could potentially result in a different prediction.

For example:

```text
Current prediction:
Loan → Rejected

Possible changes:
Credit Score: 620 → 700
Debt:         ₹80k → ₹50k

New prediction:
Loan → Approved
```

This helps answer:

> "What would need to change for the model to make a different prediction?"

---

# 💬 Conversational XAI

The central concept of TalkToModel-XAI is to make XAI **interactive**.

Instead of presenting users with a fixed explanation, users can ask follow-up questions.

### Example conversation

```text
User:
Why was this applicant rejected?

Model:
The prediction was primarily influenced by high debt
and a low credit score.

User:
Which feature had the biggest impact?

Model:
Debt had the largest positive contribution toward
the rejection prediction.

User:
What if the credit score increased?

Model:
A higher credit score would reduce the contribution
associated with credit risk, potentially changing
the prediction depending on the other features.
```

This conversational approach allows users to progressively investigate model behavior.

---

# 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Natural Language     │
                    │      Query           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Dialogue / Query     │
                    │      Parser          │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │        Explanation Engine       │
              │                                │
              │  • Feature Importance          │
              │  • Local Explanation           │
              │  • Counterfactuals             │
              │  • Model Predictions           │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │   Machine Learning   │
                    │        Model         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Human-readable       │
                    │     Explanation      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        User          │
                    └──────────────────────┘
```

---

# 📂 Repository Structure

```text
TalkToModel-XAI/
│
├── talktomodel-replication/
│   └── ...
│
├── .gitmodules
│
└── README.md
```

The main implementation is maintained inside the `talktomodel-replication` component.

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Shivwhoo/TalkToModel-XAI.git
cd TalkToModel-XAI
```

Because the project contains a Git submodule, initialize it with:

```bash
git submodule update --init --recursive
```

---

## 2. Enter the implementation directory

```bash
cd talktomodel-replication
```

The original TalkToModel implementation uses Python and provides environment/setup instructions for running its conversational XAI application.

---

## 3. Set up the environment

Create a Python environment:

```bash
conda create -n talktomodel python=3.9
conda activate talktomodel
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** Depending on the exact version of the replicated implementation and hardware configuration, dependency versions may need to be adjusted.

---

# ▶️ Running the Project

cd talktomodel-replication
source ../TalkToModel/.venv-legacy/bin/activate

```bash
python flask_app.py
```

The application provides an interface through which users can interact with supported machine-learning models using natural-language questions.

---

# 🧪 Supported ML Setting

The TalkToModel approach is primarily designed around **tabular machine-learning models and datasets**.

Typical use cases include:

- 🏥 Healthcare prediction
- 💳 Credit-risk prediction
- 🏙️ Crime prediction
- 🏦 Loan prediction
- 📊 Classification and regression problems

The original project specifically demonstrates conversational XAI on datasets including **diabetes, German credit, and COMPAS**.

---

# 🔍 What Makes This Different?

Traditional XAI:

```text
Model
  │
  ▼
Feature Importance Plot
  │
  ▼
User interprets the chart
```

Conversational XAI:

```text
Model
  │
  ▼
Explanation Engine
  │
  ▼
Natural Language
  │
  ▼
User asks questions
  │
  ▼
Follow-up explanations
```

The key difference is **interaction**.

Users don't have to understand what SHAP values, feature weights, or counterfactual distances mean before investigating a prediction.

---

# 📚 Example Questions

A conversational XAI system can support questions such as:

### Prediction

> "What did the model predict?"

### Explanation

> "Why did the model make this prediction?"

### Feature importance

> "Which features influenced the prediction the most?"

### Comparison

> "Why was this person classified differently from another person?"

### Counterfactual

> "What would need to change for the prediction to become positive?"

### Model behavior

> "How does income affect the prediction?"

### Follow-up

> "What if income increased by ₹20,000?"

---

# 🧠 Why Explainability Matters

Machine-learning models are increasingly used in high-impact domains.

A prediction alone may not be sufficient when users need to understand:

- why a decision was made,
- which information influenced it,
- whether the result is reasonable,
- what changes could affect the result,
- and whether the model behaves consistently across cases.

Explainable AI attempts to make these model behaviors more transparent.

TalkToModel-XAI explores this problem from a **human-centered, conversational perspective**.

---

# 📖 Research Paper

This repository is based on the following research:

**Dylan Slack, Satyapriya Krishna, Himabindu Lakkaraju, Sameer Singh**

> *Explaining machine learning models with interactive natural language conversations using TalkToModel*

**Nature Machine Intelligence, 2023**

DOI: `10.1038/s42256-023-00692-8`

The original paper describes TalkToModel as a conversational XAI system designed to help users understand machine-learning model predictions through natural-language interaction.

---

# 📌 Original Project

The original TalkToModel implementation and research project can be found here:

**dylan-slack/TalkToModel**

The original repository includes the application, tutorials for running the system on custom models and datasets, experiments, and development documentation.

---

# 🧪 Research Reproduction

This repository is intended as a **replication / implementation study** of the TalkToModel approach.

The goal is not only to reproduce the software but also to understand the underlying ideas behind:

```text
Natural Language
       ↓
Intent / Query Understanding
       ↓
Explanation Selection
       ↓
XAI Method
       ↓
Model Execution
       ↓
Human-readable Explanation
       ↓
Conversational Response
```

---

# 🛠️ Technology Stack

Depending on the implementation components, the project makes use of technologies in the following ecosystem:

| Technology | Purpose |
|---|---|
| 🐍 Python | Core implementation |
| 🤖 Machine Learning | Prediction models |
| 🔍 XAI | Model explanations |
| 💬 NLP | Natural-language interaction |
| 🌐 Flask | Web application |
| 📊 Tabular ML | Supported prediction setting |
| 🧪 Jupyter | Experiments / exploration |

---

# 📈 Future Improvements

Potential directions for extending the project include:

- [ ] Support additional ML model architectures
- [ ] Improve natural-language query understanding
- [ ] Add more XAI techniques
- [ ] Improve counterfactual generation
- [ ] Add visualization for explanations
- [ ] Support larger datasets
- [ ] Add conversational memory
- [ ] Improve multi-turn reasoning
- [ ] Add explanation confidence / uncertainty
- [ ] Add fairness-oriented explanations
- [ ] Build a modern web interface
- [ ] Add automated evaluation of explanation quality
- [ ] Containerize the complete application

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve the project:

```bash
# Fork the repository

# Create a new branch
git checkout -b feature/your-feature

# Make your changes

# Commit
git commit -m "Add your feature"

# Push
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📜 Citation

If you use ideas or code from the original TalkToModel research, please cite the original work:

```bibtex
@Article{Slack2023,
  author  = {Slack, Dylan and Krishna, Satyapriya and
             Lakkaraju, Himabindu and Singh, Sameer},
  title   = {Explaining machine learning models with
             interactive natural language conversations
             using TalkToModel},
  journal = {Nature Machine Intelligence},
  year    = {2023},
  month   = {Jul},
  day     = {27},
  doi     = {10.1038/s42256-023-00692-8}
}
```

---

# 👨‍💻 Authors

**Shivwhoo**

GitHub:  
https://github.com/Shivwhoo

---

# ⭐ Acknowledgements

This project is inspired by the research and open-source implementation of **TalkToModel** by:

- Dylan Slack
- Satyapriya Krishna
- Himabindu Lakkaraju
- Sameer Singh

Special thanks to the authors for making the research and implementation available to the community.

# 👨‍💻 Contributors

This project was developed by:

| Name | Roll Number |
|---|---|
| **Sachin Kumar** | 24BCS125 |
| **Sudhanshu Baberwal** | 24BCS147 |
| **Shivam Kishore** | 24BCS140 |
| **Udit Dadhich** | 24BCS158 |

---

### 🎓 Academic Project

**B.Tech — Computer Science & Engineering**  
**Indian Institute of Information Technology, Dharwad (IIIT Dharwad)**

This project was developed as part of an academic/research study on **Explainable Artificial Intelligence (XAI)** and conversational machine-learning model explanations.

---

## 📄 License

Please refer to the license and terms of the original implementation contained within the project before redistributing or modifying its code.

---

<div align="center">

### 💬 Making Machine Learning Explainable — One Conversation at a Time.

⭐ If you find this project useful, consider starring the repository.

</div>
