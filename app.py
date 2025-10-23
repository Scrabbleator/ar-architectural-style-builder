
import json
import datetime as dt
import streamlit as st

APP_TITLE = "AR.Architectural Style Builder"
st.set_page_config(page_title=APP_TITLE, layout="wide")

# ----------------------------------
# Data & Concept Guides
# ----------------------------------

STAGES = [
    {
        "id":"soul","title":"Stage 1 — Soul / Ideology",
        "prompt":"Choose the core belief(s) of your architecture.",
        "type":"multi","min_selections":1,"max_selections":2,
        "options":[
            "Order — symmetry, balance, civic duty, divine ratio",
            "Growth — organic change, evolution, breathing walls, living façades",
            "Memory — ruin, layering, patina, archaeology of time",
            "Defiance — asymmetry, rebellion, distortion, tension",
            "Transcendence — light, ascension, spirit, metaphysical space"
        ],
        "default":[
            "Order — symmetry, balance, civic duty, divine ratio",
            "Transcendence — light, ascension, spirit, metaphysical space"
        ]
    },
    {
        "id":"heritage","title":"Stage 2 — Time / Heritage",
        "prompt":"Select the ancestral lineage(s) your style imagines.",
        "type":"multi","min_selections":1,"max_selections":2,
        "options":[
            "Antiquity Reimagined — Hellenic clarity, temple logic, sacred proportion",
            "Enlightenment Rationalism — 17–18th-century civic idealism, measured geometry",
            "Neo-Spiritual Futurism — celestial materials, glass cathedrals, cosmic metaphors",
            "Forgotten Civilization — mythic ruins, invented archaeology, symbols of a lost age",
            "Timeless Modernism — pure planes, light as doctrine, austerity as prayer"
        ],
        "default":[
            "Antiquity Reimagined — Hellenic clarity, temple logic, sacred proportion",
            "Forgotten Civilization — mythic ruins, invented archaeology, symbols of a lost age"
        ]
    },
    {
        "id":"form","title":"Stage 3 — Form / Gesture",
        "prompt":"How do your buildings move and compose themselves?",
        "type":"multi","min_selections":1,"max_selections":2,
        "options":[
            "Vertical Ascent — towers, spires, and colonnades reaching skyward in disciplined rhythm",
            "Harmonic Symmetry — balanced façades, perfect ratios, temple-like calm",
            "Buried Monumentality — half-submerged mass, weight, ruins hinting at depth below",
            "Curvilinear Rebirth — domes, spirals, and arcs expressing continuity and celestial motion",
            "Fragmented Order — shards and alignments suggesting past perfection now half-remembered"
        ],
        "default":[
            "Curvilinear Rebirth — domes, spirals, and arcs expressing continuity and celestial motion",
            "Harmonic Symmetry — balanced façades, perfect ratios, temple-like calm"
        ]
    },
    {
        "id":"material","title":"Stage 4 — Material / Flesh",
        "prompt":"Pick core materials (Texture) and tones (Palette).",
        "type":"compound",
        "groups":[
            {
                "id":"texture","label":"Texture (choose 1–2)",
                "min_selections":1,"max_selections":2,
                "options":[
                    "Polished Stone — perfection, ritual, divinity through permanence",
                    "Weathered Limestone — soft endurance, faith worn by centuries",
                    "Forged Metal — strength, resonance, cosmic alloy",
                    "Carved Basalt or Obsidian — gravity, sacred darkness",
                    "Porous Ceramic or Plaster — breath, imperfection, light’s companion"
                ],
                "default":[
                    "Forged Metal — strength, resonance, cosmic alloy",
                    "Porous Ceramic or Plaster — breath, imperfection, light’s companion"
                ]
            },
            {
                "id":"tone","label":"Tone / Palette (choose 1–2)",
                "min_selections":1,"max_selections":2,
                "options":[
                    "Ivory and Gold — sanctity and enlightenment",
                    "Verdigris and Bronze — memory, oxidation, earthly transcendence",
                    "Charcoal and Ash — solemn mystery, purification through ruin",
                    "Sand and Ochre — rebirth from earth, ritual warmth",
                    "Pearl and Silver — lunar stillness, celestial reflection"
                ],
                "default":[
                    "Verdigris and Bronze — memory, oxidation, earthly transcendence",
                    "Pearl and Silver — lunar stillness, celestial reflection"
                ]
            }
        ]
    },
    {
        "id":"light","title":"Stage 5 — Light / Emotion",
        "prompt":"How does illumination behave in your spaces?",
        "type":"multi","min_selections":1,"max_selections":2,
        "options":[
            "Filtered Sanctum — light seeps through lattices or fractures, sacred and slow",
            "Radiant Core — buildings emit inner light; metallic reflection as divine aura",
            "Refracted Tide — glass, water, and reflective surfaces scatter light in motion",
            "Shadowed Silence — illumination is withheld, mystery shaped by gloom",
            "Descending Beam — light falls vertically, a connection between heaven and order"
        ],
        "default":[
            "Filtered Sanctum — light seeps through lattices or fractures, sacred and slow",
            "Descending Beam — light falls vertically, a connection between heaven and order"
        ]
    },
    {
        "id":"ornament","title":"Stage 6 — Ornament / Voice",
        "prompt":"How (if at all) do surfaces speak?",
        "type":"multi","min_selections":1,"max_selections":2,
        "options":[
            "Geometric Liturgy — repeating ratios, sacred geometry, tessellations as prayer",
            "Scriptural Reliefs — runes, calligraphy, or engraved stories folded into walls",
            "Biomorphic Reverence — vines, shells, or waves abstracted into order",
            "Fractured Inlay — kintsugi-like seams, contrasting metals marking repair and memory",
            "Silent Surface — absence of ornament, relying on proportion and light alone"
        ],
        "default":[
            "Fractured Inlay — kintsugi-like seams, contrasting metals marking repair and memory"
        ]
    },
    {
        "id":"composition","title":"Stage 7 — Composition / Signature",
        "prompt":"Choose a spatial grammar that unifies everything.",
        "type":"single",
        "options":[
            "Processional Axis — long, disciplined approaches; thresholds ascend to stillness",
            "Radial Sanctum — circular plans; all geometry converges on a luminous heart",
            "Tiered Continuum — layered terraces or ascending platforms, symbolic ascent",
            "Nested Labyrinth — sacred complexity; symmetry hiding within asymmetry",
            "Suspended Harmony — bridges or floating halls that defy gravity in balance"
        ],
        "default":"Processional Axis — long, disciplined approaches; thresholds ascend to stillness"
    }
]

CONCEPT_GUIDE = {
    "soul": {
        "Order": "Proportion, symmetry, civic clarity — classical discipline.",
        "Growth": "Biodynamic change and biomorphic forms; buildings feel alive.",
        "Memory": "Patina, layers, repair — time as material.",
        "Defiance": "Breaks grids and expectations; tension and asymmetry.",
        "Transcendence": "Light and height that point beyond the material."
    },
    "heritage": {
        "Antiquity Reimagined": "Temple logic reinterpreted; Hellenic clarity today.",
        "Enlightenment Rationalism": "18th‑century reason; measured civic ideals.",
        "Neo-Spiritual Futurism": "Cosmic metaphors, luminous media; sacred futurity.",
        "Forgotten Civilization": "Invented archaeology; mythic ruins and symbols.",
        "Timeless Modernism": "Pure planes, restraint, light-as-doctrine."
    },
    "form": {
        "Vertical Ascent": "Upward emphasis; towers and spires in rhythm.",
        "Harmonic Symmetry": "Balanced composition; calm via mirroring and ratio.",
        "Buried Monumentality": "Half-submerged mass; hints at depth/history below.",
        "Curvilinear Rebirth": "Domes/spirals; continuous, celestial motion.",
        "Fragmented Order": "Shards imply a prior whole; memory of order."
    },
    "material_texture": {
        "Polished Stone": "Ritual purity and permanence.",
        "Weathered Limestone": "Soft endurance; touch of centuries.",
        "Forged Metal": "Strength, resonance; responsive to light.",
        "Carved Basalt or Obsidian": "Gravitas; sacred darkness.",
        "Porous Ceramic or Plaster": "Breathable, imperfect; loves light."
    },
    "material_tone": {
        "Ivory and Gold": "Sanctity and enlightenment.",
        "Verdigris and Bronze": "Oxidised memory; earth meets time.",
        "Charcoal and Ash": "Purifying solemnity; shadow play.",
        "Sand and Ochre": "Earthen warmth; rebirth.",
        "Pearl and Silver": "Lunar quiet; reflective calm."
    },
    "light": {
        "Filtered Sanctum": "Screened light; devotional ambience.",
        "Radiant Core": "Glow from within; metallic aura.",
        "Refracted Tide": "Shimmer and movement from glass/water.",
        "Shadowed Silence": "Withheld light; mystery leads.",
        "Descending Beam": "Vertical shaft; heaven-to-earth axis."
    },
    "ornament": {
        "Geometric Liturgy": "Tessellations and ratios as visual prayer.",
        "Scriptural Reliefs": "Walls speak via runes/calligraphy/story.",
        "Biomorphic Reverence": "Nature abstracted into ordered motifs.",
        "Fractured Inlay": "Kintsugi seams; repair as beauty.",
        "Silent Surface": "No ornament; proportion and light suffice."
    },
    "composition": {
        "Processional Axis": "Long approach; thresholds stage stillness.",
        "Radial Sanctum": "All geometry gathers at a luminous heart.",
        "Tiered Continuum": "Ascending terraces; ritual climb.",
        "Nested Labyrinth": "Complexity with hidden symmetry.",
        "Suspended Harmony": "Bridged volumes in poised balance."
    }
}

DEFAULT_STYLE_NAME = "The Reconciliant Order"

# -------------------------------
# Utilities & State
# -------------------------------
def init_state():
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}
    if "style_name" not in st.session_state:
        st.session_state["style_name"] = DEFAULT_STYLE_NAME
    if "notes" not in st.session_state:
        st.session_state["notes"] = ""
    if "world_name" not in st.session_state:
        st.session_state["world_name"] = ""

def clean_label(s):
    return s.split(" — ")[0].strip()

def render_concept_guide(stage):
    with st.expander("Concept Guide — what the choices mean"):
        if stage["id"] == "material":
            st.markdown("**Textures**")
            for opt in stage["groups"][0]["options"]:
                n = clean_label(opt); st.markdown(f"- **{n}** — {CONCEPT_GUIDE['material_texture'][n]}")
            st.markdown("**Tones / Palette**")
            for opt in stage["groups"][1]["options"]:
                n = clean_label(opt); st.markdown(f"- **{n}** — {CONCEPT_GUIDE['material_tone'][n]}")
        else:
            key = stage["id"]
            for opt in stage["options"]:
                n = clean_label(opt)
                st.markdown(f"- **{n}** — {CONCEPT_GUIDE[key][n]}")

def render_stage(stage):
    st.subheader(stage["title"])
    st.caption(stage["prompt"])
    render_concept_guide(stage)

    if stage["type"] == "single":
        default = stage.get("default")
        value = st.radio("Pick one", options=stage["options"],
                         index=stage["options"].index(default) if default in stage["options"] else 0,
                         key=f"radio_{stage['id']}")
        st.session_state["responses"][stage["id"]] = [value]

    elif stage["type"] == "multi":
        default = stage.get("default", [])
        value = st.pills("Choose up to {} options".format(stage["max_selections"]),
                         options=stage["options"], selection_mode="multi",
                         default=default, key=f"pills_{stage['id']}")
        if len(value) < stage["min_selections"]:
            st.warning(f"Please choose at least {stage['min_selections']} option(s).")
        if len(value) > stage["max_selections"]:
            value = value[: stage["max_selections"]]
        st.session_state["responses"][stage["id"]] = value

    elif stage["type"] == "compound":
        groups = stage["groups"]
        selections = {}
        cols = st.columns(len(groups))
        for i, grp in enumerate(groups):
            with cols[i]:
                default = grp.get("default", [])
                value = st.pills(grp["label"], options=grp["options"], selection_mode="multi",
                                 default=default, key=f"pills_{stage['id']}_{grp['id']}")
                if len(value) < grp["min_selections"]:
                    st.warning(f"{grp['label']}: Choose at least {grp['min_selections']} option(s).")
                if len(value) > grp["max_selections"]:
                    value = value[: grp["max_selections"]]
                selections[grp["id"]] = value
        st.session_state["responses"][stage["id"]] = selections

def compose_manifesto(responses, style_name, notes, world_name):
    def pick(id_):
        return [clean_label(s) for s in responses.get(id_, [])]
    def pick_group(id_, group_id):
        grp = responses.get(id_, {})
        return [clean_label(s) for s in grp.get(group_id, [])]

    soul = " + ".join(pick("soul"))
    heritage = " + ".join(pick("heritage"))
    form = " + ".join(pick("form"))
    textures = ", ".join(pick_group("material", "texture"))
    tones = ", ".join(pick_group("material", "tone"))
    light = " + ".join(pick("light"))
    ornament = " + ".join(pick("ornament"))
    composition = " + ".join(pick("composition"))

    header = f"# {style_name}"
    if world_name.strip():
        header += f" — for **{world_name.strip()}**"

    manifesto = f"""{header}

**Soul / Ideology:** {soul}
**Time / Heritage:** {heritage}
**Form / Gesture:** {form}
**Material / Flesh:** {textures}
**Tone / Palette:** {tones}
**Light / Emotion:** {light}
**Ornament / Voice:** {ornament}
**Composition / Signature:** {composition}

---
**Designer Notes:** {notes or "—"}
"""
    return manifesto

def compose_prompts(responses, style_name):
    def pick(id_):
        return [clean_label(s) for s in responses.get(id_, [])]
    def pick_group(id_, group_id):
        grp = responses.get(id_, {})
        return [clean_label(s) for s in grp.get(group_id, [])]

    textures = ", ".join(pick_group("material", "texture"))
    tones = ", ".join(pick_group("material", "tone"))
    form = ", ".join(pick("form"))
    heritage = ", ".join(pick("heritage"))
    light = ", ".join(pick("light"))
    ornament = ", ".join(pick("ornament"))
    composition = ", ".join(pick("composition"))

    base = (f"{style_name} architecture, {form}, materials: {textures}, palette: {tones}, "
            f"light: {light}, ornament: {ornament}, heritage: {heritage}")

    prompts = {
        "Sacred Interior": f"interior sanctum, {base}, processional stillness, cinematic volumetric light, hyperreal detail",
        "Façade & Approach": f"monumental façade along a {composition.lower()}, {base}, wide-angle perspective, serene and mathematical",
        "Civic Plaza": f"civic plaza mixing temple and senate hall, {base}, atmospheric realism, human scale and cosmic order"
    }
    return prompts

def compose_world_outline(responses, world_name):
    name = world_name.strip() or "Unnamed World"
    def pick(id_):
        return [clean_label(s) for s in responses.get(id_, [])]
    def pick_group(id_, group_id):
        grp = responses.get(id_, {})
        return [clean_label(s) for s in grp.get(group_id, [])]

    lines = []
    lines.append(f"# World Outline — {name}")
    lines.append("")
    lines.append("## Essence")
    lines.append(f"- **Soul:** {', '.join(pick('soul')) or '—'}")
    lines.append(f"- **Heritage:** {', '.join(pick('heritage')) or '—'}")
    lines.append("")
    lines.append("## Form & Light")
    lines.append(f"- **Form:** {', '.join(pick('form')) or '—'}")
    lines.append(f"- **Light:** {', '.join(pick('light')) or '—'}")
    lines.append("")
    lines.append("## Material Language")
    lines.append(f"- **Textures:** {', '.join(pick_group('material','texture')) or '—'}")
    lines.append(f"- **Palette:** {', '.join(pick_group('material','tone')) or '—'}")
    lines.append("")
    lines.append("## Voice & Composition")
    lines.append(f"- **Ornament:** {', '.join(pick('ornament')) or '—'}")
    lines.append(f"- **Composition:** {', '.join(pick('composition')) or '—'}")
    lines.append("")
    lines.append("## Sites to Sketch")
    lines.append("- [ ] Sacred interior (altar/chamber)")
    lines.append("- [ ] Façade + processional approach")
    lines.append("- [ ] Civic plaza / forum variant")
    lines.append("")
    lines.append("## Notes")
    lines.append("_Add references, locations, climate, patrons, time period, typologies…_")
    return "\n".join(lines)

# -------------------------------
# UI
# -------------------------------
init_state()

with st.sidebar:
    st.markdown(f"### {APP_TITLE}")
    st.caption("Part of the A.R. Framework (Diadems → Architecture)")

    st.text_input("Style Name", key="style_name")
    st.text_input("World / Project Name (optional)", key="world_name")
    st.text_area("Personal Notes", key="notes", placeholder="Add references, motifs, site conditions, etc.")
    st.divider()

    st.markdown("**Preset Manager**")
    uploaded = st.file_uploader("Load preset (.json)", type=["json"], accept_multiple_files=False, label_visibility="collapsed")
    if uploaded:
        try:
            data = json.load(uploaded)
            st.session_state["style_name"] = data.get("style_name", st.session_state["style_name"])
            st.session_state["notes"] = data.get("notes", st.session_state["notes"])
            st.session_state["world_name"] = data.get("world_name", st.session_state["world_name"])
            loaded_responses = data.get("responses", {})
            if not loaded_responses and all(k in data for k in [s["id"] for s in STAGES]):
                loaded_responses = {k: data[k] for k in [s["id"] for s in STAGES] if k in data}
            st.session_state["responses"] = loaded_responses or st.session_state["responses"]
            st.success("Preset loaded. Scroll the Builder to see selections updated.")
        except Exception as e:
            st.error(f"Could not load preset: {e}")
    st.caption("Use 'Download Style JSON (Preset)' in the Builder to save your selections.")

    st.divider()
    st.markdown("**About**")
    st.caption("Use the Concept Guides to understand options before choosing. Build a style in 7 stages, export a Manifesto, AI prompts, and a World Outline.")
    st.caption("© Anselm Rajah 2025 – Co-produced with ChatGPT")

st.title(APP_TITLE)
tabs = st.tabs(["Builder", "Ornament Lab (placeholder)", "Urban Layout Lab (placeholder)"])

with tabs[0]:
    st.markdown("Use the **Concept Guide** under each stage to understand the options, then make your selections.")
    st.progress(0.0)
    progress_per_stage = 1.0 / len(STAGES)
    done = True

    for i, stage in enumerate(STAGES):
        with st.container(border=True):
            render_stage(stage)
        st.progress((i + 1) * progress_per_stage)
        resp = st.session_state["responses"].get(stage["id"])
        if stage["type"] == "single":
            if not resp or len(resp) != 1: done = False
        elif stage["type"] == "multi":
            if not resp or len(resp) < stage["min_selections"]: done = False
        elif stage["type"] == "compound":
            if not resp: done = False
            else:
                for grp in stage["groups"]:
                    selections = resp.get(grp["id"], [])
                    if len(selections) < grp["min_selections"]: done = False

    st.divider()
    col1, col2, col3 = st.columns([1,1,1])

    if done:
        manifesto = compose_manifesto(st.session_state["responses"], st.session_state["style_name"], st.session_state["notes"], st.session_state["world_name"])
        prompts = compose_prompts(st.session_state["responses"], st.session_state["style_name"])
        outline = compose_world_outline(st.session_state["responses"], st.session_state["world_name"])

        with col1:
            st.subheader("Manifesto")
            st.markdown(manifesto)

        with col2:
            st.subheader("AI Image Prompts")
            for k, v in prompts.items():
                st.markdown(f"**{k}**")
                st.code(v)

        with col3:
            st.subheader("Export")
            ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            base = (st.session_state['world_name'] or st.session_state['style_name']).replace(' ', '_')
            st.download_button("Download Manifesto (Markdown)",
                               data=manifesto.encode("utf-8"),
                               file_name=f"{base}_manifesto_{ts}.md",
                               mime="text/markdown")
            payload = {"app_title": APP_TITLE, "style_name": st.session_state["style_name"],
                       "world_name": st.session_state["world_name"],
                       "notes": st.session_state["notes"], "responses": st.session_state["responses"],
                       "prompts": prompts, "exported_at": ts}
            st.download_button("Download Style JSON (Preset)",
                               data=json.dumps(payload, indent=2).encode("utf-8"),
                               file_name=f"{base}_style_{ts}.json",
                               mime="application/json")

        st.divider()
        with st.container(border=True):
            st.subheader("World Outline")
            st.caption("A quick working document you can paste into your notebook or wiki.")
            st.markdown(outline)
            st.download_button("Download World Outline (Markdown)",
                               data=outline.encode("utf-8"),
                               file_name=f"{base}_world_outline_{ts}.md",
                               mime="text/markdown")
    else:
        st.warning("Complete all stages to generate your manifesto, prompts, and outline.")
        st.caption("Tip: Defaults are preselected — accept them and refine later.")

with tabs[1]:
    st.subheader("Ornament Lab (placeholder)")
    st.caption("Future module for motif sheets and detail prompts.")

with tabs[2]:
    st.subheader("Urban Layout Lab (placeholder)")
    st.caption("Future module for axes, plazas, and district logic.")
