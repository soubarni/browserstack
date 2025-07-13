from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, min_repetitions=2):
        self.min_repetitions = min_repetitions

    def analyze_repeated_words(self, texts):
        combined_text = ' '.join(texts).lower()
        words = re.findall(r'\w+', combined_text)
        word_counts = Counter(words)
        repeated_words = {
            word: count
            for word, count in word_counts.items()
            if count > self.min_repetitions
        }
        return repeated_words or None

