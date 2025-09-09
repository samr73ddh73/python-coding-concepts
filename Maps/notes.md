#### Initialise:
map = {}

In Python, you can’t directly do if (map[temp]) because if the key doesn’t exist, it will throw a KeyError.

### Check if key exists:

if key in map:
    return key