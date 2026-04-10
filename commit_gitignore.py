import subprocess
import sys

result = subprocess.run(
    ['git', 'commit', '-m', 'chore: add PDF output directory to .gitignore'],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
    
sys.exit(result.returncode)
