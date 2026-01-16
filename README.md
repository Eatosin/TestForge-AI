<div align="center">

# ⚛️ Zeta
### *Autonomous QA Architect & Physics-Informed Edge Case Detector*

<!-- TECH STACK BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Intelligence-Gemini_2.5-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Physics-Scikit_Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Deploy-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<!-- HERO BANNER -->
<a href="https://huggingface.co/spaces/EATosin/TestForge-AI">
  <img src="assets/zeta_hero.png" width="100%" alt="Zeta Architecture" style="border-radius: 10px; box-shadow: 0px 0px 20px rgba(0, 255, 255, 0.2); border: 1px solid #30363d;">
</a>

<br/><br/>

<!-- ACTION BUTTONS -->
<p>
  <a href="https://huggingface.co/spaces/EATosin/TestForge-AI">
    <img src="https://img.shields.io/badge/🚀_Launch_Live_App-blue?style=for-the-badge&logo=huggingface&logoColor=yellow">
  </a>
  &nbsp;
  <a href="docs/ENGINEERING_LOG.md">
    <img src="https://img.shields.io/badge/🛠️_Read_Engineering_Log-black?style=for-the-badge&logo=github">
  </a>
</p>

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
