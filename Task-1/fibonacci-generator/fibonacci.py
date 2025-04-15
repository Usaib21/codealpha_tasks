def fibonacci_generator(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

if __name__ == "__main__":
    num_terms = int(input("Enter the number of terms: "))
    fib_sequence = fibonacci_generator(num_terms)
    print("Fibonacci sequence:")
    print(fib_sequence)
