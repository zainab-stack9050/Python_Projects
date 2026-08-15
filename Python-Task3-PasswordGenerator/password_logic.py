import secrets
import string

AMBIGUOUS_CHARS = "0O1lI"

def get_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pools = {}
    if use_upper:
        pools["upper"] = string.ascii_uppercase
    if use_lower:
        pools["lower"] = string.ascii_lowercase
    if use_digits:
        pools["digits"] = string.digits
    if use_symbols:
        pools["symbols"] = "!@#$%^&*()-_=+[]{}"

    if exclude_ambiguous:
        for key in pools:
            pools[key] = "".join(c for c in pools[key] if c not in AMBIGUOUS_CHARS)

    return pools

def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pools = get_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)

    if len(pools) == 0:
        raise ValueError("At least one character type must be selected.")
    if len(pools) < 2:
        raise ValueError("At least two character types must be selected.")
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Guarantee at least one character from each selected type
    password_chars = [secrets.choice(pool) for pool in pools.values()]

    # Fill the rest randomly from the combined pool
    combined_pool = "".join(pools.values())
    remaining_length = length - len(password_chars)
    password_chars += [secrets.choice(combined_pool) for _ in range(remaining_length)]

    # Shuffle so the guaranteed characters aren't always at the start
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)

def check_strength(password):
    length = len(password)
    variety = sum([
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    ])

    if length >= 12 and variety >= 3:
        return "Strong"
    elif length >= 8 and variety >= 2:
        return "Medium"
    else:
        return "Weak"