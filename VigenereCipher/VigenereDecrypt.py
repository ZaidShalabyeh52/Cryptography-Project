import string
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

ALPHABET = string.ascii_uppercase


# Clean the text: keep only A-Z and make everything uppercase
def clean_text(text):
    return ''.join([c for c in text.upper() if c in ALPHABET])

# Find repeated sequences and calculate distances between them
def find_repeated_sequences_spacings(text, seq_len=3):
    spacing = defaultdict(list)

    for i in range(len(text) - seq_len):
        seq = text[i:i+seq_len]
        spacing[seq].append(i)

    distances = []

    # If a sequence appears more than once, calculate the gaps
    for positions in spacing.values():
        if len(positions) > 1:
            for i in range(len(positions)-1):
                distances.append(positions[i+1] - positions[i])

    return distances


# Get possible factors (possible key lengths)
def get_factors(n):
    return set(i for i in range(2, 30) if n % i == 0)


# Use Kasiski to guess likely key lengths
def kasiski_key_lengths(text):
    distances = find_repeated_sequences_spacings(text)
    factor_counts = Counter()

    for d in distances:
        for f in get_factors(d):
            factor_counts[f] += 1

    # Return most common factors
    return [k for k, _ in factor_counts.most_common(10)]


# Calculate IC (to check how close text is to English)
def index_of_coincidence(text):
    N = len(text)
    freq = Counter(text)

    if N <= 1:
        return 0

    return sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))


# Split text into columns based on key length
def split_columns(text, key_len):
    return [text[i::key_len] for i in range(key_len)]


# Calculate average IC for all columns
def avg_ic(text, key_len):
    cols = split_columns(text, key_len)
    return sum(index_of_coincidence(c) for c in cols) / key_len


# Standard English letter frequencies
EN_FREQ = {
    'E':12.7,'T':9.1,'A':8.2,'O':7.5,'I':7.0,'N':6.7,'S':6.3,'H':6.1,
    'R':6.0,'D':4.3,'L':4.0,'C':2.8,'U':2.8,'M':2.4,'W':2.4,'F':2.2,
    'G':2.0,'Y':2.0,'P':1.9,'B':1.5,'V':1.0,'K':0.8,'X':0.2,'J':0.15,
    'Q':0.1,'Z':0.07
}


# Calculate Chi-Square (how close text is to English)
def chi_squared(column):
    N = len(column)
    freq = Counter(column)

    chi = 0
    for l in ALPHABET:
        observed = freq.get(l, 0)
        expected = EN_FREQ[l] * N / 100
        chi += (observed - expected) ** 2 / (expected + 1e-9)

    return chi

# Try all shifts and pick the best one using Chi-Square
def best_shift(column):
    best = float('inf')
    best_s = 0

    for shift in range(26):
        decrypted = ''.join(
            ALPHABET[(ALPHABET.index(c) - shift) % 26]
            for c in column
        )

        score = chi_squared(decrypted)

        if score < best:
            best = score
            best_s = shift

    return best_s


# Decrypt full text using Vigenère key
def decrypt(text, key):
    out = ""
    for i, c in enumerate(text):
        shift = ALPHABET.index(key[i % len(key)])
        out += ALPHABET[(ALPHABET.index(c) - shift) % 26]
    return out

# Check common English pairs (bigrams)
def score_text(text):
    bigrams = ["TH","HE","IN","ER","AN","RE","ON","AT","EN","ND"]
    return sum(text.count(bg) * 5 for bg in bigrams)


# Compare column frequency with English frequency
def plot_column_freq(column, key, key_len, col_index):
    freq = Counter(column)
    total = len(column)

    letters = list(ALPHABET)

    cipher_vals = [(freq.get(l, 0) / total) * 100 for l in letters]
    english_vals = [EN_FREQ[l] for l in letters]

    x = range(len(letters))

    plt.figure()

    plt.bar(x, cipher_vals, width=0.4, label="Ciphertext")
    plt.bar([i + 0.4 for i in x], english_vals, width=0.4, label="English")

    plt.xticks([i + 0.2 for i in x], letters)

    plt.title(f"Column {col_index+1}\nKey: {key} | Key Length: {key_len}")
    plt.legend()

    plt.show()


# Take input from user
cipher_input = input("Paste cipher text: ").strip()

# Clean the input
cipher = clean_text(cipher_input)

if not cipher:
    raise ValueError("No valid cipher text entered.")

print("\n🔍 Running analysis...\n")

# Get key length candidates using Kasiski
kasiski = kasiski_key_lengths(cipher)

# Get best IC values
ic_scores = {k: avg_ic(cipher, k) for k in range(2, 15)}
top_ic = sorted(ic_scores, key=ic_scores.get, reverse=True)[:5]

# Combine both methods
candidates = list(set(kasiski + top_ic))

best = ("", "", -1, 0)

# -------- FIND BEST KEY --------
for key_len in candidates:

    cols = split_columns(cipher, key_len)
    key = ""

    # Find shift for each column
    for col in cols:
        key += ALPHABET[best_shift(col)]

    # Decrypt text
    plaintext = decrypt(cipher, key)

    # Score result
    score = score_text(plaintext)

    print(f"Key Length {key_len} → KEY: {key} | Score: {score}")

    # Save best result
    if score > best[2]:
        best = (key, plaintext, score, key_len)

# -------- FINAL OUTPUT --------
best_key, best_text, _, best_len = best

print("\n==============================")
print("BEST KEY:", best_key)
print("KEY LENGTH:", best_len)
print("\nPLAINTEXT PREVIEW:\n")
print(best_text[:1000])
print("\n==============================")

# -------- PLOT ONLY BEST --------
print("\nGenerating frequency graphs for BEST key...\n")

best_columns = split_columns(cipher, best_len)

for i, col in enumerate(best_columns):
    plot_column_freq(col, best_key, best_len, i)
