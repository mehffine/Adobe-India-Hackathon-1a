from typing import List, Dict

class OutlineHierarchy:
    @staticmethod
    def build(items: List[Dict]) -> List[Dict]:
        """Convert flat heading list into nested sequence keeping order."""
        stack: List[str] = []
        for it in items:
            lvl = it["level"]
            # maintain stack depth
            while stack and lvl <= stack[-1]:
                stack.pop()
            stack.append(lvl)
            it["level"] = lvl  # already correct
        return items  # flat list is enough per schema
