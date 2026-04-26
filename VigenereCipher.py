"""Manual substitution helper for Vigenere-style ciphertext analysis.

Edit the MAP_* variables below. Example:
MAP_Q = "E"
This will place "E" under every Q in the ciphertext output.
"""

# Manual per-letter mapping (leave empty to show underscore "_")
MAP_A = ""
MAP_B = ""
MAP_C = ""
MAP_D = ""
MAP_E = "H"
MAP_F = ""
MAP_G = ""
MAP_H = "T"
MAP_I = ""
MAP_J = ""
MAP_K = ""
MAP_L = ""
MAP_M = ""
MAP_N = ""
MAP_O = ""
MAP_P = ""
MAP_Q = ""
MAP_R = ""
MAP_S = ""
MAP_T = ""
MAP_U = ""
MAP_V = ""
MAP_W = ""
MAP_X = ""
MAP_Y = ""
MAP_Z = ""

CHUNK_SIZE = 100

SUBSTITUTION_MAP = {
    "A": MAP_A,
    "B": MAP_B,
    "C": MAP_C,
    "D": MAP_D,
    "E": MAP_E,
    "F": MAP_F,
    "G": MAP_G,
    "H": MAP_H,
    "I": MAP_I,
    "J": MAP_J,
    "K": MAP_K,
    "L": MAP_L,
    "M": MAP_M,
    "N": MAP_N,
    "O": MAP_O,
    "P": MAP_P,
    "Q": MAP_Q,
    "R": MAP_R,
    "S": MAP_S,
    "T": MAP_T,
    "U": MAP_U,
    "V": MAP_V,
    "W": MAP_W,
    "X": MAP_X,
    "Y": MAP_Y,
    "Z": MAP_Z,
}


def normalize_map_value(value):
    """Return a single uppercase letter mapping or underscore placeholder."""
    if not value:
        return "_"

    candidate = str(value).strip().upper()
    if len(candidate) != 1 or not candidate.isalpha():
        return "_"

    return candidate


def build_normalized_map():
    """Build a safe A-Z map where each entry is one letter or underscore."""
    normalized = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        normalized[letter] = normalize_map_value(SUBSTITUTION_MAP.get(letter, ""))
    return normalized


def mapped_line_for_chunk(chunk, normalized_map):
    """Create a line of mapped letters (or underscores) for a ciphertext chunk."""
    mapped_chars = []
    for ch in chunk:
        upper_ch = ch.upper()
        if upper_ch.isalpha():
            mapped_chars.append(normalized_map.get(upper_ch, "_"))
        else:
            mapped_chars.append("_")
    return "".join(mapped_chars)


def main():
    print("Vigenere Cipher Helper")
    print("Paste ciphertext and press Enter:")
    ciphertext = input().rstrip("\n")

    if not ciphertext:
        print("No ciphertext provided.")
        return

    normalized_map = build_normalized_map()

    print("\nOutput (50 characters per block):\n")
    for start in range(0, len(ciphertext), CHUNK_SIZE):
        chunk = ciphertext[start:start + CHUNK_SIZE]
        print(chunk)
        print(mapped_line_for_chunk(chunk, normalized_map))
        print()


if __name__ == "__main__":
    main()
