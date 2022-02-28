# Coding Challenge 3.1: Simple Directory Tree

# Replicate this tree of directories and subdirectories:
# ├── draft_code
# |   ├── pending
# |   └── complete
# ├── includes
# ├── layouts
# |   ├── default
# |   └── post
# |       └── posted
# └── site

import os
import shutil

os.makedirs("C:/draft_code/pending")
os.mkdir("C:/draft_code/complete")
os.mkdir("C:/includes")
os.makedirs("C:/layouts/default")
os.makedirs("C:/layouts/post/posted")
os.mkdir("C:/site")

shutil.rmtree("C:/draft_code")
shutil.rmtree("C:/layouts")
os.rmdir("C:/includes")
os.rmdir("C:/site")