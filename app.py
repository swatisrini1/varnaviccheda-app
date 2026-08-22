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


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="वर्ण विच्छेद", page_icon="🕉️")

st.title("🕉️ वर्णविच्छेद: (Varna Viccheda)")
st.write("Enter a Devanagari word to see its letter-by-letter split.")

word = st.text_input("शब्दं लिखतु / Enter word:", value="रामः")

if word.strip():
    try:
        result = varna_viccheda(word.strip())
        st.markdown("### Result:")
        st.markdown(f"## {result}")
    except Exception as e:
        st.error(f"Could not process this input: {e}")
else:
    st.info("Type a word above to see the result.")

st.markdown("---")
st.caption("Built for Shastra course demonstration.")
