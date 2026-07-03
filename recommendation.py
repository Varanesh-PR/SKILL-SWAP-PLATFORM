def recommend(skill):
    suggestions = {
        "python": ["machine learning", "data science"],
        "guitar": ["music theory", "singing"]
    }

    return suggestions.get(skill.lower(), [])