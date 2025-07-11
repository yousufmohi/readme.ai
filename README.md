<div align="center">

# README.ai

<p align="">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original.svg" alt="React" width="50" height="50" style="margin-right: 20px;" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/npm/npm-original-wordmark.svg" alt="npm" width="50" height="50" style="margin-right: 20px;" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="50" height="50" style="margin-right: 20px;" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg" alt="FastAPI" width="50" height="50" style="margin-right: 20px;" />
  <img src="https://avatars.githubusercontent.com/u/140009580?s=200&v=4" alt="Groq" width="50" height="50" style="margin-right: 20px;" />
</p>

Create a new production-ready **README** with just the link of your **GitHub** repository. Keep writing code and creating projects, README.ai will take care of the README.

</div>


---

## Prerequisites

Make sure you have the following installed:

- ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
- ![Node.js](https://img.shields.io/badge/Node.js-LTS-green?logo=node.js&logoColor=white)
- ![npm](https://img.shields.io/badge/npm-v9+-CB3837?logo=npm&logoColor=white)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yousufmohi/readme.ai
cd readme.ai
````

### 2. Run the setup script

#### On macOS/Linux:

```bash
./setup.sh
```

#### On Windows (PowerShell):

```powershell
./setup.ps1
```

## Technical Description

The project uses a **FastAPI** backend with the **Groq** API to generate the README. For larger files the business logic ignores certain files that may be in the repository like ```pycache``` and chunks the files to get the general idea of which technologies are used and other important information. The project uses a **React** and **TypeScript** frontend which has two displays, one with the ```README``` and one with the markdown, letting you do live updates if the generated readme was not what you expected.






