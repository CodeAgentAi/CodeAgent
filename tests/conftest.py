import os
import sys

# So that we can do `import codeagentai in our tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import codeagentai # noqa: E402

codeagent.api_base = os.getenv("CODEAGENT_API_BASE")  # type: ignore
codeagent.api_key = os.getenv("CODEAGENT_API_KEY")  # type: ignore
