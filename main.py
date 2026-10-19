print("Hello World")
data = {
    "class2608": {"Alice": 85, "Bob": 90},
    "class2609": {"Charlie": 78, "David": 88}
}
scores = [s for cls in data for s in data[cls].values()]
print(max(scores))
print()
print(sum(scores) / len(scores))