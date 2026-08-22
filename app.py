import streamlit as st

# ---------------- Core logic (from your notebook) ----------------

matra_to_vowel = {
    "":  "अ",   # inherent vowel, no visible sign
    "ा": "आ",
    "ि": "इ",
    "ी": "ई",
    "ु": "उ",
    "ू": "ऊ",
    "ृ": "ऋ",
    "ॄ": "ॠ",
    "ॢ": "ऌ",
    "ॣ": "ॡ",
    "े": "ए",
    "ै": "ऐ",
    "ो": "ओ",
    "ौ": "औ",
    '्': "",
    "ं": "ं",
    "ः": "ः"
}

consonants = ["क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ",
              "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न",
              "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व",
              "श", "ष", "स", "ह"]

matras = ["ा", "ि", "ी", "ु", "ू", "ृ", "ॄ", "ॢ", "ॣ", "े", "ै", "ो", "ौ", '्', 'ं', 'ः']

vowels = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ"]


def varna_viccheda(padam: str) -> str:
    """Return the varna-viccheda (letter split) of a Devanagari word."""
    result = []
    length = len(padam)

    for i in range(length):
        ch = padam[i]

        if ch in ['ं', 'ः'] and i > 0 and padam[i - 1] in consonants:
            result.append('अ')
            result.append(ch)

        elif ch in consonants and (i + 1 == length or padam[i + 1] not in matras):
            result.append(ch + '्')
            result.append('अ')

        elif ch in matras:
            result.append(matra_to_vowel[ch])

        elif ch in vowels:
            result.append(ch)

        else:
            result.append(ch + '्')

    return " ".join(result)


def purvarupa_sandhi(word: str) -> list:
    """Split a word containing avagraha (ऽ) and restore the elided अ
    following the पूर्वरूप सन्धि rule (े/ो + avagraha)."""
    if "ऽ" not in word:
        raise ValueError("Word does not contain avagraha (ऽ). Example: हरेऽत्र")

    pp_up = word.split("ऽ")

    if len(pp_up) != 2 or not pp_up[0] or not pp_up[1]:
        raise ValueError("Word should have exactly one avagraha, with text on both sides. Example: हरेऽत्र")

    if pp_up[0].endswith("े"):
        pp_up[1] = 'अ' + pp_up[1]
    elif pp_up[0].endswith("ो"):
        pp_up[0] = pp_up[0][:-1] + 'ः'
        pp_up[1] = 'अ' + pp_up[1]
    else:
        raise ValueError("पूर्वरूप rule applies only when the word before ऽ ends in े or ो.")

    return pp_up

def vowel_assign(matra: str):
    """Map a matra sign to its independent vowel form (empty string -> अ)."""
    matra_to_vowel_map = {
        "ा": "आ", "ि": "इ", "ी": "ई", "ु": "उ", "ू": "ऊ",
        "ृ": "ऋ", "ॄ": "ॠ", "ॢ": "ऌ", "ॣ": "ॡ",
        "े": "ए", "ै": "ऐ", "ो": "ओ", "ौ": "औ", "": "अ"
    }
    return matra_to_vowel_map.get(matra)


def vowel_to_matra(vowel: str):
    """Map an independent vowel form back to its matra sign (अ -> empty string)."""
    vowel_to_matra_map = {
        "अ": "", "आ": "ा", "इ": "ि", "ई": "ी", "उ": "ु", "ऊ": "ू",
        "ऋ": "ृ", "ॠ": "ॄ", "ऌ": "ॢ", "ॡ": "ॣ", "ए": "े", "ऐ": "ै", "ओ": "ो", "औ": "ौ"
    }
    return vowel_to_matra_map.get(vowel)


def savarna_deergha_sandhi(purvapada: str, uttarapada: str) -> str:
    """Join two words using सवर्ण दीर्घ सन्धि (similar vowels -> long vowel)."""
    savarna_rules = {
        'अ': 'आ', 'आ': 'आ',
        'इ': 'ई', 'ई': 'ई',
        'उ': 'ऊ', 'ऊ': 'ऊ',
        'ऋ': 'ॠ', 'ऌ': 'ॠ'
    }

    if not purvapada or not uttarapada:
        raise ValueError("Please enter both the first and second word.")

    consonants_str = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'

    v1_char = purvapada[-1]
    if v1_char in consonants_str:
        v1 = 'अ'
    else:
        v1 = vowel_assign(v1_char)

    v2 = uttarapada[0]

    if v1 is None or v2 not in savarna_rules:
        raise ValueError("Could not identify valid vowels at the junction. Example: रमा + आगच्छति")

    if v1 not in savarna_rules or v2 not in savarna_rules or savarna_rules[v1] != savarna_rules[v2]:
        raise ValueError(f"सवर्ण दीर्घ सन्धि does not apply between '{v1}' and '{v2}'. "
                          f"It applies only when both vowels belong to the same अ/इ/उ/ऋ group.")

    merged_vowel = savarna_rules[v1]
    result_matra = vowel_to_matra(merged_vowel)

    p = purvapada[:-1] if v1 != 'अ' else purvapada
    u = uttarapada[1:]

    return p + result_matra + u
# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="संस्कृतोपयोगिनि उपकरणानि", page_icon="🕉️")

st.title(" संस्कृतोपयोगिनि उपकरणानि (Sanskrit Tools)")

tab1, tab2, tab3 = st.tabs(["वर्णविच्छेदः", "पूर्वरूपसन्धिः"])

with tab1:
    st.subheader("वर्णविच्छेदः (Varna Viccheda)")
    st.write("Enter a Devanagari word to see its letter-by-letter split.")

    word = st.text_input("शब्दं लिखतु / Enter word:", value="रामः", key="vv_input")

    if word.strip():
        try:
            result = varna_viccheda(word.strip())
            st.markdown("### Result:")
            st.markdown(f"## {result}")
        except Exception as e:
            st.error(f"Could not process this input: {e}")
    else:
        st.info("Type a word above to see the result.")

with tab2:
    st.subheader("पूर्वरूपसन्धिः (Purvarupa Sandhi)")
    st.write("Enter a word with avagraha (ऽ) to split it back into its two original words.")

    pp_word = st.text_input("शब्दं लिखतु / Enter word:", value="हरेऽत्र", key="pp_input")

    if pp_word.strip():
        try:
            parts = purvarupa_sandhi(pp_word.strip())
            st.markdown("### Result:")
            st.markdown(f"## {parts[0]} + {parts[1]}")
        except ValueError as e:
            st.error(str(e))
    else:
        st.info("Type a word above to see the result.")
with tab3:
    st.subheader("सवर्णदीर्घसन्धि: (Savarna Deergha Sandhi)")
    st.write("Enter two words to join them when their vowels at the junction are savarna (same group).")

    col1, col2 = st.columns(2)
    with col1:
        purvapada = st.text_input("पूर्वपदम् / First word:", value="रमा", key="sd_purva")
    with col2:
        uttarapada = st.text_input("उत्तरपदम् / Second word:", value="आगच्छति", key="sd_uttara")

    if purvapada.strip() and uttarapada.strip():
        try:
            joined = savarna_deergha_sandhi(purvapada.strip(), uttarapada.strip())
            st.markdown("### Result:")
            st.markdown(f"## {purvapada} + {uttarapada} = {joined}")
        except ValueError as e:
            st.error(str(e))
    else:
        st.info("Enter both words above to see the result.")

st.markdown("---")
st.caption("Built for Shastra course demonstration.")
