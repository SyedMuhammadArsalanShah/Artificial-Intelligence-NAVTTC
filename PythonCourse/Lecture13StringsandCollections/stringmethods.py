
### Python String Methods with Examples

# String capitalize()
text = "syed muhammad arsalan shah"
print(text.capitalize())  # Output: 'Syed muhammad arsalan shah'

# String casefold()
text = "SYED MUHAMMAD ARSALAN SHAH"
print(text.casefold())  # Output: 'syed muhammad arsalan shah'

# String center()
text = "Syed"
print(text.center(20, '-'))  # Output: '-------Syed--------'

# String count()
text = "Syed Muhammad Arsalan Shah"
print(text.count("a"))  # Output: 5

# String encode()
text = "Syed"
print(text.encode())  # Output: b'Syed'

# String endswith()
text = "Syed Muhammad Arsalan Shah"
print(text.endswith("Shah"))  # Output: True

# String expandtabs()
text = "Syed\tMuhammad"
print(text.expandtabs(10))  # Output: 'Syed      Muhammad'

# String find()
text = "Syed Muhammad Arsalan Shah"
print(text.find("Muhammad"))  # Output: 5

# String format()
text = "My name is {}"
print(text.format("Syed Muhammad Arsalan Shah"))  # Output: 'My name is Syed Muhammad Arsalan Shah'

# String format_map()
data = {"name": "Syed"}
text = "My name is {name}"
print(text.format_map(data))  # Output: 'My name is Syed'

# String index()
text = "Syed Muhammad Arsalan Shah"
print(text.index("Muhammad"))  # Output: 5

# String isalnum()
text = "Syed123"
print(text.isalnum())  # Output: True

# String isalpha()
text = "Syed"
print(text.isalpha())  # Output: True

# String isdecimal()
text = "12345"
print(text.isdecimal())  # Output: True

# String isdigit()
text = "12345"
print(text.isdigit())  # Output: True

# String isidentifier()
text = "Syed123"
print(text.isidentifier())  # Output: True

# String islower()
text = "syed"
print(text.islower())  # Output: True

# String isnumeric()
text = "12345"
print(text.isnumeric())  # Output: True

# String isprintable()
text = "Syed\n"
print(text.isprintable())  # Output: False

# String isspace()
text = "   "
print(text.isspace())  # Output: True

# String istitle()
text = "Syed Muhammad"
print(text.istitle())  # Output: True

# String isupper()
text = "SYED"
print(text.isupper())  # Output: True

# String join()
text = ["Muhammad", "Arsalan", "Shah"]
print(" ".join(text))  # Output: 'Muhammad Arsalan Shah'

# String ljust()
text = "Syed"
print(text.ljust(10, '-'))  # Output: 'Syed------'

# String lower()
text = "SYED"
print(text.lower())  # Output: 'syed'

# String lstrip()
text = "   Syed"
print(text.lstrip())  # Output: 'Syed'

# String maketrans()
translation = str.maketrans("m", "W")
text = "mom"
print(text.translate(translation))  # Output: 'Syed'

# String partition()
text = "Syed Muhammad Arsalan Shah"
print(text.partition("Muhammad"))  # Output: ('Syed ', 'Muhammad', ' Arsalan Shah')

# String replace()
text = "Syed Muhammad"
print(text.replace("Muhammad", "Arsalan"))  # Output: 'Syed Arsalan'

# String rfind()
text = "Syed Muhammad Arsalan Shah"
print(text.rfind("a"))  # Output: 24

# String rindex()
text = "Syed Muhammad Arsalan Shah"
print(text.rindex("a"))  # Output: 24

# String rjust()
text = "Syed"
print(text.rjust(10, '-'))  # Output: '------Syed'

# String rpartition()
text = "Syed Muhammad Arsalan Shah"
print(text.rpartition("Muhammad"))  # Output: ('Syed ', 'Muhammad', ' Arsalan Shah')

# String rsplit()
text = "Syed Muhammad Arsalan Shah"
print(text.rsplit(" ", 2))  # Output: ['Syed Muhammad', 'Arsalan', 'Shah']

# String rstrip()
text = "Syed   "
print(text.rstrip())  # Output: 'Syed'

# String split()
text = "Syed Muhammad Arsalan Shah"
print(text.split())  # Output: ['Syed', 'Muhammad', 'Arsalan', 'Shah']

# String splitlines()
text = "Syed\nMuhammad\nArsalan Shah"
print(text.splitlines())  # Output: ['Syed', 'Muhammad', 'Arsalan Shah']

# String startswith()
text = "Syed Muhammad"
print(text.startswith("Syed"))  # Output: True

# String strip()
text = "   Syed   "
print(text.strip())  # Output: 'Syed'

# String swapcase()
text = "Syed Muhammad"
print(text.swapcase())  # Output: 'sYED mUHAMMAD'

# String title()
text = "syed muhammad arsalan shah"
print(text.title())  # Output: 'Syed Muhammad Arsalan Shah'

# String translate()
translation = str.maketrans("a", "@")
text = "arsalan"
print(text.translate(translation))  # Output: '@rs@l@n'

# String upper()
text = "syed"
print(text.upper())  # Output: 'SYED'

# String zfill()
text = "123"
print(text.zfill(5))  # Output: '00123'