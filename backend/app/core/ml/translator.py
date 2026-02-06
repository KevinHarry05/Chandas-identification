# Simple translation dictionary for Chandas names

CHANDAS_TRANSLATIONS = {
    "अनुष्टुभ्": {
        "english": "Anushtubh",
        "tamil": "அனுஷ்டுப் சந்தஸ்",
        "hindi": "अनुष्टुप छंद"
    },
    "त्रिष्टुप्": {
        "english": "Trishtubh",
        "tamil": "திருஷ்டுப் சந்தஸ்",
        "hindi": "त्रिष्टुप छंद"
    },
    "वसन्ततिलका": {
    "english": "Vasantatilaka",
    "tamil": "வசந்ததிலகா சந்தஸ்",
    "hindi": "वसंततिलका छंद"
},

    "जगती": {
        "english": "Jagati",
        "tamil": "ஜகதி சந்தஸ்",
        "hindi": "जगती छंद"
    }
}

def translate_chandas(chandas_name: str) -> dict:
    return CHANDAS_TRANSLATIONS.get(
        chandas_name,
        {
            "english": "Unknown",
            "tamil": "தெரியாதது",
            "hindi": "अज्ञात"
        }
    )
