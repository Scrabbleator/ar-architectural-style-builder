
# AR.Architectural Style Builder (with Concept Guides + World Outline)

A Streamlit app to define a unique architectural dialect in 7 stages, with **Concept Guides** explaining each option before you choose. Exports a **Manifesto**, **AI image prompts**, and a **World Outline**. Includes a **Preset Manager** to save/load styles (JSON).

## Local Run (macOS / Windows / Linux)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Preset Manager
- **Save preset:** In the Builder tab, click **Download Style JSON (Preset)**.
- **Load preset:** In the sidebar, use **Load preset (.json)** to restore your selections and notes.

## Deploy to Streamlit Community Cloud
1. Create a GitHub repo named `ar-architectural-style-builder`.
2. Add these files: `app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md`.
3. In Streamlit Community Cloud, click **New app**, select your repo, and choose `app.py`.
4. Deploy, then bookmark the live URL in Safari.
