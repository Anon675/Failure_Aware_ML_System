import os

tests = [
    "test_routing.py",
    "test_signals.py",
    "test_logs.py",
    "test_human_review.py",
    "test_video_short.py",
    "test_video_normal.py"
]

for test in tests:
    print(f"\nRunning {test}")
    os.system(f"python tests/{test}")
