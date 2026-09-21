# DEPLOYMENT GUIDE — NEXUS AI

NEXUS AI is fully optimized for **₹0 free deployment** on **Streamlit Community Cloud**.

---

## 1. Local Development Instructions

### Step 1: Clone & Setup Workspace
```bash
git clone https://github.com/your-username/NEXUS-AI.git
cd NEXUS-AI
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Data Generator & Train Models
```bash
python scripts/generate_demo_data.py
python scripts/train_models.py
python scripts/build_graph.py
```

### Step 4: Run Tests
```bash
python scripts/run_tests.py
```

### Step 5: Launch Streamlit Application
```bash
python -m streamlit run app/app.py
```

---

## 2. Streamlit Community Cloud Free Deployment (Step-by-Step)

1. Push your repository to **GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of NEXUS AI"
   git branch -M main
   git remote add origin https://github.com/your-username/NEXUS-AI.git
   git push -u origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app**.
4. Select your repository: `your-username/NEXUS-AI`.
5. Set Branch to: `main`.
6. Set Main file path to: `app/app.py`.
7. Click **Deploy!**

The application will start automatically loading packaged data and lightweight model artifacts. Zero secret API keys or GPU instances are required.
