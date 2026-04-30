import string
from collections import Counter

ALPHABET = string.ascii_uppercase

COMMON_WORDS = ["THE", "AND", "TO", "OF", "IN", "THAT", "IS", "WITH", "FOR"]

def clean_text(text):
    return ''.join([c for c in text.upper() if c in ALPHABET])

def split_columns(text, key_len):
    return [text[i::key_len] for i in range(key_len)]

def chi_squared(column):
    # English letter frequency
    expected_freq = {
        'E':12.7,'T':9.1,'A':8.2,'O':7.5,'I':7.0,'N':6.7,'S':6.3,'H':6.1,
        'R':6.0,'D':4.3,'L':4.0,'C':2.8,'U':2.8,'M':2.4,'W':2.4,'F':2.2,
        'G':2.0,'Y':2.0,'P':1.9,'B':1.5,'V':1.0,'K':0.8,'X':0.2,'J':0.15,
        'Q':0.1,'Z':0.07
    }
    
    total = len(column)
    freq = Counter(column)
    
    chi = 0
    for letter in ALPHABET:
        observed = freq.get(letter, 0)
        expected = expected_freq[letter] * total / 100
        chi += ((observed - expected) ** 2) / (expected + 0.0001)
    
    return chi

def best_shift(column):
    best = float('inf')
    best_shift = 0
    
    for shift in range(26):
        decrypted = ""
        for c in column:
            decrypted += ALPHABET[(ALPHABET.index(c) - shift) % 26]
        
        score = chi_squared(decrypted)
        
        if score < best:
            best = score
            best_shift = shift
    
    return best_shift

def decrypt(cipher, key):
    plaintext = ""
    for i, c in enumerate(cipher):
        shift = ALPHABET.index(key[i % len(key)])
        plaintext += ALPHABET[(ALPHABET.index(c) - shift) % 26]
    return plaintext

def score_text(text):
    score = 0
    for word in COMMON_WORDS:
        score += text.count(word) * 10
    return score

cipher = """HWIUBVYVRVWDAHVHYCSQREGKFIVYRVXRRRJREGIDFIGXEMXBCSPLPCFDFIHRAYWHEMHHAXMIVGEWVSRLQVITHMVHGLEWPPMHAXWBFXIPFEYWUIRWVGEWRXLHZWIOIIWWBWIUIIVVOYXWEYWWGLIFYMIQGWCVGIQFBRGHERMQTXLHVHIQGMXBBJMWFYWHEVITHMVHGLIXFIVWBTVRIILLFSVKRVMGRRXLGCJREIEFUWIUIMGHVRZRXIHDYWSURUYLEIXKNXWHEZIUFTVRIIXKRMVLQIRWVXCWBGPLRRXVVREVZEPOPPSVRHIQIMVRAQIQGMRZUMGKNPPVLWXHZWEURSAQRHEQQSTHEEXHQFCDFMRJYISUTERLMEXLBRXKRJMUFXSUCIVKNTWWUIWHPSRGFXVDGIKBZECVHJJLPIFXGMRDZSVHBTIQRRZLESRPRRXLAALLPLRHGASUXGSQAIGWVSRVGSSWUIVPNGLLAIWDEIWXCTSUGIHWUIXKVVHDCTVRNGLLFRIHQIHWBTVRGIGWHWIUVRJREQEWVSRDAHVHFSYUPIWKBYWHQEXWUIWHEZIUXIVERVSVFYTSBVXVGLMVGLMUQETSESEFUOIUOIVRFEWVHQIVNHMVGVMEHXIGPPMHAXWHEZIUNVGKVXIFGYVHNRHHZTPRLWSQRSVPBVINRVFHESWVRVZHEWXRCVSYVHIDAEYWUIRWVGEWVSRVRVZLPIXKRJMUFXTXOPMVUIHURTSUGSRNRVFHESWVGIMOVWXHQXLHSSPOBAMQTVITHMVHZIRWFWIFHVIDAIXZBVOHNZIVQVSSCIVVUSYOQRSWOIEEYIXRBFXDVRXKRRIFRWWDECMQSSVPNXMRAXSLZTIUFSRDGIEXFIVPBVIJRRIUNPPBXIVERVSVFLSXYHFHFXVRAKIQBYKKGLEWNTSWRRXLNPSSCSRHAXHRRWRRGJMQQMXWBFIWUIAHNOPLAOVHYMEEYIJREEPOFIVYVGIVGLEWEIPBBROHEFIUBWJREEGFRWWFBRXUBPPDPOSINZELYEFLYMXBBJXKROIUOIVRFWIUIMGHZIEQFPEFXSJDIEMONFMOVXCRSXLHFYTSBVXHQWIUIMGHFLIQPIOHEFIUBWWKBYPGOILLTLPBEIPLNFPHNRHVUSYOQIQSYSCDQMWWEMFXGIHVRVZHEEVFUMXHPXYURAMWUSRHFCWWRQEEYIXROEGNHTEQBXLHEXVDAWTDEIRWVHIDYPCWUIYVRVWKBYPGASXEREADEIXKNXEXGLIQGMGDGMSQVWXDXMRJCPEFRFIBBRHWUIVHDYMURQIQGXSHAXIUNTEVFASUQ"""
cipher = clean_text(cipher)

best_overall = ("", "", 0)

for key_len in range(2, 13):
    columns = split_columns(cipher, key_len)
    
    key = ""
    for col in columns:
        shift = best_shift(col)
        key += ALPHABET[shift]
    
    plaintext = decrypt(cipher, key)
    score = score_text(plaintext)
    
    print(f"Key length {key_len}: {key} | Score: {score}")
    
    if score > best_overall[2]:
        best_overall = (key, plaintext, score)

print("\n===== BEST RESULT =====")
print("KEY:", best_overall[0])
print("PLAINTEXT PREVIEW:\n", best_overall[1][:500])