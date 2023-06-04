class MathSamples:
    @staticmethod
    def fibonacci(n):
        if n == 0:
            return 0
        elif n <= 2:
            return 1
        else:
            return MathSamples.fibonacci(n-1) + \
                    MathSamples.fibonacci(n-2)