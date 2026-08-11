from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from review_v2.blind_runner import main


if __name__ == "__main__":
    main()
