# app.py
import streamlit as st
import re
import time

st.set_page_config(page_title="FLAMES Game", page_icon="🔥", layout="centered")

def clean_name(name: str) -> list:
    """Lowercase, remove non-letters and spaces, return list of letters."""
    name = name.lower()
    name = re.sub(r'[^a-z]', '', name)
    return list(name)

def remove_common_letters(a: list, b: list) -> (list, list):
    """Remove letters present in both lists (one-to-one)."""
    a_copy = a.copy()
    b_copy = b.copy()
    i = 0
    while i < len(a_copy):
        ch = a_copy[i]
        if ch in b_copy:
            a_copy.pop(i)
            b_copy.remove(ch)
            # don't increment i because list shifted
        else:
            i += 1
    return a_copy, b_copy

def flames_result(name1: str, name2: str, show_steps=False):
    a = clean_name(name1)
    b = clean_name(name2)
    a_rem, b_rem = remove_common_letters(a, b)
    count = len(a_rem) + len(b_rem)

    if show_steps:
        st.write("Cleaned names (letters only):")
        st.write(f"{name1!r} → {''.join(a) or '(empty)'}")
        st.write(f"{name2!r} → {''.join(b) or '(empty)'}")
        st.write("After removing common letters:")
        st.write(f"Remaining from 1: {''.join(a_rem) or '(none)'}")
        st.write(f"Remaining from 2: {''.join(b_rem) or '(none)'}")
        st.write(f"Total letters remaining: **{count}**")
        st.write("---")

    if count == 0:
        # special case: all letters cancelled
        return "All letters cancel out — strong bond! (Result: **Siblings / Close**)"

    flames = list("FLAMES")  # F L A M E S
    steps = []
    idx = 0
    while len(flames) > 1:
        # position to remove: (count-1) steps from current idx (0-based)
        remove_index = (idx + count - 1) % len(flames)
        removed = flames.pop(remove_index)
        steps.append((remove_index, removed, flames.copy()))
        # next start index is remove_index (already points to next element after pop)
        idx = remove_index % len(flames) if flames else 0

    final_letter = flames[0]
    meaning = {
        "F": "Friends",
        "L": "Love",
        "A": "Affection",
        "M": "Marriage",
        "E": "Enemy",
        "S": "Siblings"
    }[final_letter]

    if show_steps:
        st.write("Elimination steps (index, removed letter, remaining):")
        for stepnum, (i_removed, r_letter, remaining) in enumerate(steps, start=1):
            st.write(f"{stepnum:>2}. Remove index {i_removed} → **{r_letter}**  → Remaining: {''.join(remaining)}")
        st.write("---")

    return f"Result: **{final_letter} — {meaning}**"

# --- Streamlit UI ---
st.title("🔥 FLAMES Game")
st.write("Enter two names and press **Check** to find out the FLAMES result.")

with st.form(key="flames_form"):
    col1, col2 = st.columns(2)
    with col1:
        name1 = st.text_input("Name 1", value="", placeholder="e.g. Alice")
    with col2:
        name2 = st.text_input("Name 2", value="", placeholder="e.g. Bob")

    options_col1, options_col2 = st.columns([1, 3])
    with options_col1:
        show_steps = st.checkbox("Show steps", value=False)
    with options_col2:
        animate = st.checkbox("Play little animation", value=True)

    submitted = st.form_submit_button("Check FLAMES")

if submitted:
    if not name1.strip() or not name2.strip():
        st.error("Please enter both names (non-empty).")
    else:
        with st.spinner("Calculating..."):
            # Optional visual animation (small, non-blocking)
            if animate:
                progress = st.progress(0)
                for p in range(0, 101, 20):
                    time.sleep(0.06)
                    progress.progress(p)
                progress.empty()

            result_text = flames_result(name1, name2, show_steps=show_steps)

        # friendly card-like display
        st.markdown("### 🔮 FLAMES Result")
        st.markdown(f"**{name1.strip().title()}**  &nbsp;&nbsp; **{name2.strip().title()}**")
        st.success(result_text)

        # small friendly message mapped to meaning
        mapping_text = {
            "Friends": "You're likely to be good friends!",
            "Love": "Romance is in the air 💘",
            "Affection": "Warm feelings and fondness.",
            "Marriage": "A match made for long-term!",
            "Enemy": "Watch out — playful rivalry or tension.",
            "Siblings": "A very close/familial bond."
        }
        # parse final meaning
        m = re.search(r"—\s(.+?)\*\*", result_text)
        if m:
            meaning_key = m.group(1).strip()
            st.info(mapping_text.get(meaning_key, ""))

st.write("---")
st.caption("Classic FLAMES game — for fun only. Not scientifically meaningful 😉")
