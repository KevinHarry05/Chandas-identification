from app.core.ml.sanskrit_prosody import syllabify, laghu_guru

def main():
    verse = "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ"

    syllables = syllabify(verse)
    pattern = laghu_guru(syllables)

    print("Verse:")
    print(verse)
    print("\nSyllables:")
    print(syllables)
    print("\nLaghu-Guru Pattern:")
    print(pattern)

if __name__ == "__main__":
    main()
