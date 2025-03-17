# GSB Model GitHub

The **GSB Model GitHub** repository, created by [Nikitas Rigas Kalogeropoulos](https://github.com/kalogeropo), is a Python-based project focused on **data mining** and **information retrieval models**.

---

## 📌 Table of Contents

- [GSB Model GitHub](#gsb-model-github)
  - [📌 Table of Contents](#-table-of-contents)
  - [📥 Installation](#-installation)
    - [🔹 1️⃣ Clone the repository:](#-1️⃣-clone-the-repository)
    - [🔹 2️⃣ Install dependencies:](#-2️⃣-install-dependencies)
  - [🚀 Usage](#-usage)
  - [📂 Project Structure](#-project-structure)
    - [📁 Directories:](#-directories)
    - [📜 Key Python Scripts:](#-key-python-scripts)
  - [📌 Citations](#-citations)

---

## 📥 Installation

To set up the project environment, follow these steps:

### 🔹 1️⃣ Clone the repository:

```
git clone https://github.com/kalogeropo/Gsb_model.git
cd Gsb_model
```


### 🔹 2️⃣ Install dependencies:

Ensure you have Python installed. Then, install the required Python packages:

```
pip install -r requirements.txt
```


---

## 🚀 Usage

To execute the main script, run the following command:

```
python main_v2.py
```


> **Note:** Each script performs the experiments described in the repective publication. Review the scripts before execution to understand their specific functionalities.

---

## 📂 Project Structure

The repository contains the following primary components:

### 📁 Directories:


- **`Preprocess/`** - Contains preprocessing scripts and tools.
- **`experiments/`** - Includes experimental the collections of Cystic Fibrosis, Cranfield, NPL as well as test collection for debugging purposes.
- **`models/`** - Houses model definitions and related files.
- **`utilities/`** - Provides utility functions and helpers.


### 📜 Key Python Scripts:

- **`Debug_and_testing.py`** - Script for debugging and testing purposes.
- **`GSB_testing.py`** - Related to GSB model testing.
- **`GoW_testing.py`** - Pertains to GoW model testing.
- **`apriori_eval.py`** - Script for evaluating Apriori algorithms.
- **`borda_percentage_gsb.py`** - Implements Borda count with percentage windowed GSB and simple GSB.
- **`borda_vazir_gsb.py`** - Combines GoW and GSB.
- **`inverted_index_creation.py`** - Script to create inverted indices.


⚙ Configuration and Requirements:

- **`.gitignore`** - Specifies files and directories to be ignored by Git.
- **`requirements.txt`** - Lists Python dependencies for the project.
- **`Collections`** - The necessary collections for benchmarking are located in the experiments folder.
---
## 📌 Citations

  - Kalogeropoulos, N.-R., Skamnelos, N., & Makris, C. (2025). On the Graph-Based Extension of the Set-Based Model: A New Approach on Graph Representation and Model Ensemble. DOI: 10.21203/rs.3.rs-3801152/v1

  - Kalogeropoulos, N.-R., Ioannou, D., Stathopoulos, D., & Makris, C. (2024). On Embedding Implementations in Text Ranking and Classification Employing Graphs. Electronics, 13(10), 1897. DOI: 10.3390/electronics13101897

  - Kalogeropoulos, N.-R., Ioannou, D., & Makris, C. (2024). Spectral Clustering and Query Expansion Using Embeddings on Graph-Based Information Retrieval Models. Expert Systems with Applications. DOI: 10.1016/j.eswa.2024.125771

  - Kalogeropoulos, N.-R., Doukas, I., Makris, C., & Kanavos, A. (2020). A Graph-Based Extension for the Set-Based Model Implementing Algorithms Based on Important Nodes. In Artificial Intelligence Applications and Innovations. AIAI 2020 IFIP WG 12.5 International Workshops (pp. 143–154). Springer. DOI: 10.1007/978-3-030-49190-1_13
