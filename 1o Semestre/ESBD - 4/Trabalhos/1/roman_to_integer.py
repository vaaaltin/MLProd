class RomanToInteger():
    @staticmethod
    def romanToInt(s: str) -> int:
        romanos = {
            "I":1,
            "V":5,
            "X":10,
            "L":50,
            "C":100,
            "D":500,
            "M":1000,
            "IV":4,
            "IX":9,
            "XL":40,
            "XC":90,
            "CD":400,
            "CM":900
        }

        i = 0
        num = 0
        following_numbers = 1

        while(i<len(s)):
            if s[i] not in romanos:
                return 'NA'
            
            if i>0:
                if s[i]==s[i-1]:
                    following_numbers += 1
                    if following_numbers == 4:
                        return 'NA'
                else:
                    following_numbers = 1

                if romanos[s[i]] > romanos[s[i-1]] and romanos[s[i-1]] != 1:
                    return 'NA'
                
            if i+1<len(s) and s[i:i+2] in romanos:
                num += romanos[s[i:i+2]]
                i += 2
            else:
                num += romanos[s[i]]
                i += 1
            
        return num
