# ============================================================
# Enhanced Feature Engineering for Chandas Classification
# ============================================================

import pandas as pd
from collections import Counter
import numpy as np
from math import log2


def extract_enhanced_features(pattern: str) -> dict:
    """
    Extract comprehensive features from Laghu-Guru pattern.
    
    Enhanced features include:
    - Basic counts (length, G/L counts, ratio)
    - N-gram frequencies (bigrams, trigrams, 4-grams)
    - Pattern statistics (runs, alternations, entropy)
    - Position-based features (start/end/middle patterns)
    - Rhythm patterns (periodicity, symmetry)
    - Advanced metrics (pattern entropy, complexity scores)
    
    Args:
        pattern: String of L and G characters
    
    Returns:
        Dictionary of numerical features (30+ features)
    """
    
    if not pattern or not isinstance(pattern, str):
        raise ValueError("Invalid pattern")
    
    pattern_length = len(pattern)
    guru_count = pattern.count("G")
    laghu_count = pattern.count("L")
    
    # Basic features
    guru_laghu_ratio = (
        guru_count / laghu_count if laghu_count > 0 else float(guru_count)
    )
    
    guru_percentage = guru_count / pattern_length if pattern_length > 0 else 0
    laghu_percentage = laghu_count / pattern_length if pattern_length > 0 else 0
    
    # N-gram features (bigrams)
    bigrams = [pattern[i:i+2] for i in range(len(pattern)-1)]
    bigram_counts = Counter(bigrams)
    
    gg_count = bigram_counts.get('GG', 0)
    ll_count = bigram_counts.get('LL', 0)
    gl_count = bigram_counts.get('GL', 0)
    lg_count = bigram_counts.get('LG', 0)
    
    # Trigram features
    trigrams = [pattern[i:i+3] for i in range(len(pattern)-2)]
    trigram_counts = Counter(trigrams)
    
    ggg_count = trigram_counts.get('GGG', 0)
    lll_count = trigram_counts.get('LLL', 0)
    glg_count = trigram_counts.get('GLG', 0)
    lgl_count = trigram_counts.get('LGL', 0)
    
    # 4-gram features (NEW)
    fourgrams = [pattern[i:i+4] for i in range(len(pattern)-3)] if len(pattern) >= 4 else []
    fourgram_counts = Counter(fourgrams)
    glgl_count = fourgram_counts.get('GLGL', 0)
    lgly_count = fourgram_counts.get('LGLG', 0)
    ggll_count = fourgram_counts.get('GGLL', 0)
    llgg_count = fourgram_counts.get('LLGG', 0)
    
    # Run lengths (consecutive same syllables)
    max_guru_run = 0
    max_laghu_run = 0
    avg_guru_run = 0
    avg_laghu_run = 0
    current_run = 1
    guru_runs = []
    laghu_runs = []
    
    for i in range(1, len(pattern)):
        if pattern[i] == pattern[i-1]:
            current_run += 1
        else:
            if pattern[i-1] == 'G':
                guru_runs.append(current_run)
                max_guru_run = max(max_guru_run, current_run)
            else:
                laghu_runs.append(current_run)
                max_laghu_run = max(max_laghu_run, current_run)
            current_run = 1
    
    # Update last run
    if pattern:
        if pattern[-1] == 'G':
            guru_runs.append(current_run)
            max_guru_run = max(max_guru_run, current_run)
        else:
            laghu_runs.append(current_run)
            max_laghu_run = max(max_laghu_run, current_run)
    
    # Average run lengths (NEW)
    avg_guru_run = np.mean(guru_runs) if guru_runs else 0
    avg_laghu_run = np.mean(laghu_runs) if laghu_runs else 0
    
    # Alternation count (switches between G and L)
    alternations = sum(1 for i in range(1, len(pattern)) if pattern[i] != pattern[i-1])
    alternation_rate = alternations / pattern_length if pattern_length > 1 else 0
    
    # Position-based features (first, middle, and last segments)
    quarter_len = max(1, pattern_length // 4)
    start_pattern = pattern[:quarter_len]
    middle_pattern = pattern[pattern_length//2 - quarter_len//2 : pattern_length//2 + quarter_len//2] if pattern_length >= 4 else pattern
    end_pattern = pattern[-quarter_len:]
    
    start_g_count = start_pattern.count('G')
    middle_g_count = middle_pattern.count('G')
    end_g_count = end_pattern.count('G')
    
    start_g_ratio = start_g_count / len(start_pattern) if start_pattern else 0
    middle_g_ratio = middle_g_count / len(middle_pattern) if middle_pattern else 0
    end_g_ratio = end_g_count / len(end_pattern) if end_pattern else 0
    
    # Pattern complexity (variety of n-grams)
    bigram_variety = len(bigram_counts)
    trigram_variety = len(trigram_counts)
    fourgram_variety = len(fourgram_counts)
    
    # Entropy calculation (NEW) - measures pattern unpredictability
    def calculate_entropy(counts):
        total = sum(counts.values())
        if total == 0:
            return 0
        probs = [count/total for count in counts.values()]
        return -sum(p * log2(p) if p > 0 else 0 for p in probs)
    
    entropy_bigram = calculate_entropy(bigram_counts)
    entropy_trigram = calculate_entropy(trigram_counts)
    
    # Symmetry score (NEW) - check if pattern is symmetric
    reverse_pattern = pattern[::-1]
    symmetry_score = sum(1 for i in range(len(pattern)) if pattern[i] == reverse_pattern[i]) / pattern_length if pattern_length > 0 else 0
    
    # Rhythmic periodicity (NEW) - detect repeating patterns
    def find_period(s):
        """Find shortest repeating period in pattern"""
        n = len(s)
        for period in range(1, n // 2 + 1):
            if n % period == 0:
                repeats = n // period
                substring = s[:period]
                if substring * repeats == s:
                    return period
        return n
    
    pattern_period = find_period(pattern)
    is_periodic = pattern_period < pattern_length
    periodicity_ratio = pattern_period / pattern_length if pattern_length > 0 else 1
    
    # Weighted positional encoding (NEW)
    weighted_g_position = sum((i+1) for i, char in enumerate(pattern) if char == 'G') / (pattern_length * guru_count) if guru_count > 0 else 0
    weighted_l_position = sum((i+1) for i, char in enumerate(pattern) if char == 'L') / (pattern_length * laghu_count) if laghu_count > 0 else 0
    
    # Compile all features
    features = {
        # Basic features (5)
        "pattern_length": float(pattern_length),
        "guru_count": float(guru_count),
        "laghu_count": float(laghu_count),
        "guru_laghu_ratio": float(guru_laghu_ratio),
        "laghu_percentage": float(laghu_percentage),
        
        # Percentage features (1)
        "guru_percentage": float(guru_percentage),
        
        # Bigram features (4)
        "gg_count": float(gg_count),
        "ll_count": float(ll_count),
        "gl_count": float(gl_count),
        "lg_count": float(lg_count),
        
        # Trigram features (4)
        "ggg_count": float(ggg_count),
        "lll_count": float(lll_count),
        "glg_count": float(glg_count),
        "lgl_count": float(lgl_count),
        
        # 4-gram features (4) NEW
        "glgl_count": float(glgl_count),
        "lglg_count": float(lgly_count),
        "ggll_count": float(ggll_count),
        "llgg_count": float(llgg_count),
        
        # Run features (4) - 2 new
        "max_guru_run": float(max_guru_run),
        "max_laghu_run": float(max_laghu_run),
        "avg_guru_run": float(avg_guru_run),
        "avg_laghu_run": float(avg_laghu_run),
        
        # Pattern dynamics (2) - 1 new
        "alternations": float(alternations),
        "alternation_rate": float(alternation_rate),
        
        # Position features (6) - 4 new
        "start_g_count": float(start_g_count),
        "middle_g_count": float(middle_g_count),
        "end_g_count": float(end_g_count),
        "start_g_ratio": float(start_g_ratio),
        "middle_g_ratio": float(middle_g_ratio),
        "end_g_ratio": float(end_g_ratio),
        
        # Complexity features (5) - 3 new
        "bigram_variety": float(bigram_variety),
        "trigram_variety": float(trigram_variety),
        "fourgram_variety": float(fourgram_variety),
        "entropy_bigram": float(entropy_bigram),
        "entropy_trigram": float(entropy_trigram),
        
        # Symmetry and rhythm features (4) NEW
        "symmetry_score": float(symmetry_score),
        "pattern_period": float(pattern_period),
        "periodicity_ratio": float(periodicity_ratio),
        "is_periodic": float(1.0 if is_periodic else 0.0),
        
        # Weighted positional features (2) NEW
        "weighted_g_position": float(weighted_g_position),
        "weighted_l_position": float(weighted_l_position),
    }
    
    return features


def build_enhanced_feature_df(pattern: str) -> pd.DataFrame:
    """
    Build DataFrame with enhanced features for a single pattern.
    
    Args:
        pattern: Laghu-Guru pattern string
    
    Returns:
        DataFrame with all features
    """
    features = extract_enhanced_features(pattern)
    return pd.DataFrame([features])


if __name__ == "__main__":
    # Test feature extraction
    test_pattern = "LGLGLLGGLGLLLLGG"
    
    features = extract_enhanced_features(test_pattern)
    
    print("Enhanced Feature Extraction Test")
    print("=" * 60)
    print(f"Pattern: {test_pattern}")
    print(f"Pattern Length: {len(test_pattern)}")
    print(f"\nTotal Features: {len(features)}")
    print("\nFeature Values:")
    for name, value in features.items():
        print(f"  {name:20} = {value:.3f}")
