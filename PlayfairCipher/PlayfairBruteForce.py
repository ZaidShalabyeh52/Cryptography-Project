import wordninja
def generate_matrix(key):
    key = key.upper().replace("J", "I")
    keyintomatrix = []

    for c in key:
        if c not in keyintomatrix:
            keyintomatrix.append(c)

    for i in range(65, 91):
        char = chr(i)
        if char == 'J':
            continue
        if char not in keyintomatrix:
            keyintomatrix.append(char)

    matrix = [keyintomatrix[i*5:(i+1)*5] for i in range(5)]
    return matrix



def indexlocator(matrix, x):
    if x == 'J':
        x = 'I'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == x:
                return [i, j]



def decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    text = ciphertext

    i = 0
    while i < len(text) - 1:
        if text[i] == text[i+1]:
            text = text[:i+1] + 'X' + text[i+1:]
        i += 2

    if len(text) % 2 != 0:
        text += 'X'

    result = ""
    i = 0

    while i < len(text):
        a = indexlocator(matrix, text[i])
        b = indexlocator(matrix, text[i+1])

        if a[1] == b[1]:
            result += matrix[(a[0]-1) % 5][a[1]]
            result += matrix[(b[0]-1) % 5][b[1]]
        elif a[0] == b[0]:
            result += matrix[a[0]][(a[1]-1) % 5]
            result += matrix[b[0]][(b[1]-1) % 5]
        else:
            result += matrix[a[0]][b[1]]
            result += matrix[b[0]][a[1]]

        i += 2

    return result



def score_text(text):
    common = "ETAOINSHRDLU"  
    score = 0
    for c in text:
        if c in common:
            score += 1
    return score



ciphertext = input("Enter ciphertext: ").replace(" ", "").upper()

letters ="abcdefghijklmnopqrstuvwxyz"

best_score = -1
best_text = ""
best_key = ""

for a in letters:
    for b in letters:
        for c in letters:
            key = a + b + c

            plaintext = decrypt(ciphertext, key)
            s = score_text(plaintext)

            if s > best_score:
                best_score = s
                best_text = plaintext
                best_key = key


print("\n=== FINAL ANSWER ===")
print("Key:", best_key.upper())
print("Plaintext:", best_text)
print("Words   :", " ".join(wordninja.split(best_text)))