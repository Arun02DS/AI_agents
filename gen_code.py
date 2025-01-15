def generate_fibonacci(n: int) -> list:
    """
    Generate the Fibonacci series up to the nth number.

    Args:
        n (int): The number of terms in the Fibonacci series.

    Returns:
        list: A list of Fibonacci numbers up to the nth term.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is less than or equal to 0.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be a positive integer")

    def fibonacci_generator():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    def multiply_matrices(a, b):
        result = [[0, 0], [0, 0]]
        result[0][0] = a[0][0] * b[0][0] + a[0][1] * b[1][0]
        result[0][1] = a[0][0] * b[0][1] + a[0][1] * b[1][1]
        result[1][0] = a[1][0] * b[0][0] + a[1][1] * b[1][0]
        result[1][1] = a[1][0] * b[0][1] + a[1][1] * b[1][1]
        return result

    def matrix_power(matrix, n):
        if n == 1:
            return matrix
        if n % 2 == 0:
            half_pow = matrix_power(matrix, n // 2)
            return multiply_matrices(half_pow, half_pow)
        else:
            half_pow = matrix_power(matrix, n // 2)
            return multiply_matrices(multiply_matrices(half_pow, half_pow), matrix)

    if n <= 100:  # Use generator for smaller values of n
        fib_sequence = []
        fib_gen = fibonacci_generator()
        for _ in range(n):
            fib_sequence.append(next(fib_gen))
        return fib_sequence
    else:  # Use matrix exponentiation method for larger values of n
        fib_matrix = [[1, 1], [1, 0]]
        result_matrix = matrix_power(fib_matrix, n - 1)
        fib_sequence = [0, 1]
        for i in range(2, n):
            fib_sequence.append(result_matrix[0][0])
        return fib_sequence

import unittest

class TestGenerateFibonacci(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(generate_fibonacci(1), [0])
        self.assertEqual(generate_fibonacci(2), [0, 1])

    def test_large_input(self):
        self.assertEqual(generate_fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            generate_fibonacci("10")
        with self.assertRaises(ValueError):
            generate_fibonacci(-1)

    def test_large_n(self):
        self.assertEqual(generate_fibonacci(100), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836310543, 2971213707, 4807524247, 7778737960, 12586262193, 20365029324, 32951301509, 53316330799, 86267632310, 139583963111, 225850293415, 365434256549, 591284549957, 956718806499, 1548003356466, 2504720162967, 4052723519438, 6557443682403, 10610167201901, 17157603925914, 27767771127800, 44925375053691, 72693146181663, 117620521235349, 190323992452006, 307944513687301, 498268506139331, 806212919826543, 1304481421965847, 2105692545331806, 3410173967297660, 5515866512629472, 8926039479927160, 14441905992556624, 23397470791828183, 37839376784384790, 61236847576212882, 99076224360597655, 160313071936810473, 259685315242787203, 419998387179597656, 679683702422384849, 1099682089602982538, 1779610921380572400, 2879293010983554908, 4658903932364127327, 7538196943347681685, 12197100875711809047, 19724270209088586007, 31921371084800394929, 51645641293888981159, 83567012378689376109, 135212653662578357215, 218878776449471138349, 354091430111749495566, 572969206560220633915, 927060636671970128454, 1499030843232190762310, 2425092919949896855709, 3924123763182087618016, 6349216683131984473720, 10273340446314070891637, 16606510767766891288968, 26879851214080962180601, 43486361981787853469570, 70366213195868715650171, 113852575177656568919669, 184514706835343725520243, 298367282012999894439905, 482881988848343620060123, 781249270861343514500128, 1264131259709687134560220, 2047063548323119275657221, 3311194808032806405217440, 5358268356355925670874661, 8679463164398732076089910, 14037731520754657146238553, 22705099231379524693222102, 36742830752134181839460502, 59447929983513706532682648, 96190760735647888372143148, 155638690619161694910823716, 251546297975639577760675695, 407185088594800831511849555, 658731386570440308272525230])

if __name__ == "__main__":
    unittest.main()

'''
The code includes comprehensive unit tests using the `unittest` module to verify the correctness of the `generate_fibonacci` function. You can run 
the tests by executing the script.

Example use cases:

*   Generate the first 10 Fibonacci numbers: `generate_fibonacci(10)`
*   Generate the first 100 Fibonacci numbers: `generate_fibonacci(100)`
*   Test the function with invalid input: `generate_fibonacci("10")` or `generate_fibonacci(-1)`
'''