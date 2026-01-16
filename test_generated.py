# Quick test of generated math.py

# Read and execute the generated file
with open("examples/math.py", "r") as f:
    exec(f.read())

# Test the functions
result1 = add(2, 3)
result2 = multiply(4, 5)

print(f"add(2, 3) = {result1}")
print(f"multiply(4, 5) = {result2}")
print()

# Verify success criteria
assert result1 == 5, f"Expected 5, got {result1}"
assert result2 == 20, f"Expected 20, got {result2}"
print("✓ All assertions passed!")
print("✓ add(2, 3) == 5 confirmed!")
