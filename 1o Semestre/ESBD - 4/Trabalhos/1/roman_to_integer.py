class RomanToInteger():
    @staticmethod
    def romanToInt(roman):
        roman_values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        total = 0
        prev_value = 0
        following_numbers = 1

        for i in range(len(roman) - 1, -1, -1):
            current_value = roman_values[roman[i]]

            if current_value >= prev_value:
                total += current_value
            # elif current_value < prev_value and current_value != 1:
            #     return 'NA'
            else:
                total -= current_value
            
            #check if have more than 3 numbers in sequence
            if prev_value == current_value:
                following_numbers+=1
                if following_numbers > 3:
                    return 'NA'
            else:
                following_numbers = 1
            print('i: ', i)
            print('anterior: ', prev_value)
            print('atual: ', current_value)
            prev_value = current_value

        return total

