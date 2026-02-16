"""
Debug script to test TextClip and find the issue
Run this to see what's happening with TextClip
"""

from moviepy import TextClip

print("Testing TextClip with different parameter combinations...\n")

# Test 1: Minimal parameters
print("Test 1: Minimal TextClip")
try:
    clip1 = TextClip("Hello", fontsize=32)
    print("✓ Success with minimal parameters")
    clip1.close()
except Exception as e:
    print(f"✗ Error: {e}\n")

# Test 2: With font parameter
print("\nTest 2: TextClip with font")
try:
    clip2 = TextClip("Hello", fontsize=32, font='Arial')
    print("✓ Success with font parameter")
    clip2.close()
except Exception as e:
    print(f"✗ Error: {e}\n")

# Test 3: With all your parameters
print("\nTest 3: TextClip with all parameters (like your code)")
try:
    clip3 = TextClip(
        "Hello World",
        fontsize=32,
        color='white',
        bg_color='black',
        font='Arial',
        method='caption',
        size=(600, None)
    )
    print("✓ Success with all parameters")
    clip3.close()
except Exception as e:
    print(f"✗ Error: {e}\n")

# Test 4: Check TextClip signature
print("\nTest 4: Checking TextClip function signature")
import inspect
sig = inspect.signature(TextClip)
print(f"TextClip parameters: {sig}")

# Test 5: Try the alternative syntax without 'method'
print("\nTest 5: TextClip without method parameter")
try:
    clip5 = TextClip(
        "Hello World",
        fontsize=32,
        color='white',
        bg_color='black',
        font='Arial',
        size=(600, None)
    )
    print("✓ Success without method parameter")
    clip5.close()
except Exception as e:
    print(f"✗ Error: {e}\n")

print("\n" + "="*50)
print("Debug complete! Check which tests passed above.")
