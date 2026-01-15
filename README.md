<div align="center">

# ⚛️ Zeta
### *Autonomous QA Architect & Physics-Informed Edge Case Detector*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Intelligence-Gemini_2.5-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](https://ai.google.dev)
[![Scikit-Learn](https://img.shields.io/badge/Physics-Scikit_Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

[Live Demo](https://huggingface.co/spaces/EATosin/TestForge-AI) • [Engineering Log](docs/ENGINEERING_LOG.md) • [User Guide](docs/USER_GUIDE.md) • [Architecture](docs/architecture.md)

</div>

---

## ⚡ The Problem: "Happy Path" Testing
Most automated test generators only cover the "Happy Path"—the expected user behavior. They miss the **Edge Cases**: the statistical anomalies and boundary conditions that cause 90% of production outages.

## 🧠 The Solution: Physics-Informed QA
**Zeta** is not just an LLM wrapper. It is a hybrid system that combines **Generative AI** (for creativity) with **Statistical Physics** (for rigor).

It calculates the **Complexity Z-Score** of every software requirement. If a requirement is statistically "dense" (high logic complexity) but has low test coverage, Zeta flags it as a **Critical Risk**.

---

## 🆚 Comparison: Why Zeta?

| Feature | Standard LLM Gen | ⚛️ Zeta (Physics Engine) |
| :--- | :--- | :--- |
| **Generation** | Hallucinates generic tests | uses **Gemini 2.5** with SOTA Prompting |
| **Validation** | None (Blind trust) | **IsolationForest + Z-Score** Anomaly Detection |
| **Safety** | Returns broken JSON often | **Pydantic Type-Safety** & Self-Healing |
| **Output** | Text descriptions | Executable **Selenium/Python** Code |

---

## 📚 Documentation Index
*   **[Engineering Log](docs/ENGINEERING_LOG.md):** A deep dive into the bugs we fought (NumPy ambiguity, Data Loss) and how we fixed them. **(Must Read for Engineers)**.
*   **[User Guide](docs/USER_GUIDE.md):** Step-by-step instructions on generating tests and interpreting Z-Scores.
*   **[System Architecture](docs/architecture.md):** High-level diagrams of the FastAPI/Streamlit microservice topology.

---

## 🛠️ Tech Stack
*   **Core:** Python 3.11, FastAPI, Uvicorn
*   **ML Engine:** Scikit-Learn (Isolation Forest), NumPy (Vectorization)
*   **Frontend:** Streamlit, Altair (Visualization)
*   **Infrastructure:** Docker, Hugging Face Spaces

## 👨‍💻 Author
**Owadokun Tosin Tobi**
*Senior AI Engineer & Physicist*
