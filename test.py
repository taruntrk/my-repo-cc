import traceback
try:
    raise ValueError("")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    print(traceback.format_exc())
