from collections import Counter

def get_text_input():
    """Get text input from user"""
    text = input("ENTER TEXT: ")
    text = text.upper()
    text = text.replace(" ", "")
    return text

def analyze_frequency(text, n_gram):
    """
    Analyze frequency of n-grams in text
    n_gram: 1 for single characters, 2 for digraphs, etc.
    Returns sorted list of (element, count) tuples
    """
    # Extract n-grams from text
    ngrams = [text[i:i+n_gram] for i in range(len(text) - n_gram + 1)]
    
    # Count frequencies
    freq_counter = Counter(ngrams)
    
    # Sort by frequency (descending) then alphabetically
    sorted_freq = sorted(freq_counter.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_freq

def analyze_trigrams_ignore_extra(text):
    """Analyze overlapping trigrams and ignore trailing incomplete chars."""
    trigrams = [text[i:i+3] for i in range(len(text) - 2)]

    freq_counter = Counter(trigrams)
    sorted_freq = sorted(freq_counter.items(), key=lambda x: (-x[1], x[0]))

    return sorted_freq

def display_frequency(sorted_freq, n_gram):
    """Display frequency analysis results"""
    gram_type = "CHARACTER" if n_gram == 1 else f"{n_gram}-GRAM"
    
    print(f"\n{gram_type} FREQUENCY ANALYSIS:")
    print("-" * 40)
    print(f"{'Rank':<6} {gram_type:<10} {'Count':<10} {'Percentage':<10}")
    print("-" * 40)
    
    total = sum(count for _, count in sorted_freq)
    
    for rank, (element, count) in enumerate(sorted_freq, 1):
        percentage = (count / total) * 100
        print(f"{rank:<6} {element:<10} {count:<10} {percentage:.2f}%")
    
    print("-" * 40)

def display_top_n(sorted_freq, n_gram, top_count=10):
    """Display only top N most frequent elements"""
    gram_type = "CHARACTER" if n_gram == 1 else f"{n_gram}-GRAM"
    
    print(f"\nTOP {top_count} MOST FREQUENT {gram_type}S:")
    print("-" * 40)
    
    total = sum(count for _, count in sorted_freq)
    
    for rank, (element, count) in enumerate(sorted_freq[:top_count], 1):
        percentage = (count / total) * 100
        bar = "█" * (count // 2) if count > 0 else ""
        print(f"{rank:<3} {element:<5} : {bar} {count} ({percentage:.2f}%)")
    
    print("-" * 40)

def main():
    while True:
        print("\n" + "="*40)
        print("FREQUENCY ANALYZER")
        print("="*40)
        
        text = get_text_input()
        
        if not text:
            print("Please enter valid text!")
            continue
        
        print("\nANALYSIS OPTIONS:")
        print("1. Single Character Frequency")
        print("2. Digraph (2-Character) Frequency")
        print("3. Both Analyses")
        print("4. Trigram (3-Character) Frequency")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            freq = analyze_frequency(text, 1)
            display_frequency(freq, 1)
            display_top_n(freq, 1, 10)
            
        elif choice == "2":
            freq = analyze_frequency(text, 2)
            display_frequency(freq, 2)
            display_top_n(freq, 2, 10)
            
        elif choice == "3":
            freq_1 = analyze_frequency(text, 1)
            display_frequency(freq_1, 1)
            display_top_n(freq_1, 1, 10)
            
            freq_2 = analyze_frequency(text, 2)
            display_frequency(freq_2, 2)
            display_top_n(freq_2, 2, 10)
            
        elif choice == "4":
            freq_3 = analyze_trigrams_ignore_extra(text)
            display_frequency(freq_3, 3)
            display_top_n(freq_3, 3, 10)

        elif choice == "5":
            break
            
        else:
            print("Invalid choice! Please select 1-5.")
        
        cont = input("\nContinue? (y/n): ").strip().lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
