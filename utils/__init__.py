def unqualifiedName(name: str) -> str:
    """Remove namespace qualifier from tagnames"""
    i = name.find('}')
    if i == -1:
        # Name is unqualified already
        return name
    return name[i+1:]