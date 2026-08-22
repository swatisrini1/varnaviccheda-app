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


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="संस्कृत उपकरण", page_icon="🕉️")

st.title("🕉️ संस्कृत उपकरण (Sanskrit Tools)")

tab1, tab2 = st.tabs(["वर्ण विच्छेद", "पूर्वरूप सन्धि"])

with tab1:
    st.subheader("वर्ण विच्छेद (Varna Viccheda)")
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
    st.subheader("पूर्वरूप सन्धि (Purvarupa Sandhi)")
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

st.markdown("---")
st.caption("Built for Shastra course demonstration.")
