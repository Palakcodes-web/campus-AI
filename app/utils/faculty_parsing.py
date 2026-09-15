import re


# Group tags like:
# (C1), (C2), (C3), (C4)
# (GP1), (GP2), (Gp1), (Gp2)
_GROUP_TAG = re.compile(
    r"\(\s*([A-Za-z]{1,4}\d+)\s*\)",
    re.IGNORECASE,
)


def normalize_name_key(name: str) -> str:
    """
    Used for faculty de-duplication.

    Example:
        Dr. D.K. Dhir
        Dr D.K. Dhir

    Both normalize to the same key.
    """
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse_faculty_field(raw: str):
    """
    Convert faculty text into:

        [(name, group, needs_verification), ...]

    Examples:

        "Dr ABC"
        ->
        [("Dr ABC", None, False)]

        "Dr ABC & Ms XYZ"
        ->
        [
            ("Dr ABC", None, False),
            ("Ms XYZ", None, False)
        ]

        "Dr ABC, Ms XYZ"
        ->
        [
            ("Dr ABC", None, False),
            ("Ms XYZ", None, False)
        ]

        "Dr ABC / Ms XYZ"
        ->
        [
            ("Dr ABC", None, False),
            ("Ms XYZ", None, False)
        ]

    Group information is preserved when explicitly present.
    """

    if not raw or not raw.strip():
        return []

    text = raw.strip()

    # ---------------------------------------------------------
    # CASE 1: Explicit group-tagged faculty
    # ---------------------------------------------------------
    #
    # Example:
    #   "Prof A (GP1), Prof B (GP2)"
    #
    # or:
    #   "Prof A (C1), Prof B (C2)"
    #
    tagged = list(_GROUP_TAG.finditer(text))

    if tagged:
        results = []

        # Find faculty immediately before each group tag.
        previous_end = 0

        for match in tagged:
            group = match.group(1).upper()

            before = text[previous_end:match.start()]

            # Remove separators left by previous segment
            before = before.strip(" ,/&+")

            if before:
                # If there is a separator inside the segment,
                # split it into names only when clearly separable.
                parts = re.split(
                    r"\s*(?:,|&|\+|/)\s*",
                    before
                )

                parts = [
                    p.strip(" ,/&+")
                    for p in parts
                    if p.strip(" ,/&+")
                ]

                if len(parts) == 1:
                    results.append(
                        (parts[0], group, False)
                    )
                else:
                    # Multiple names mapped to same explicit group
                    for part in parts:
                        results.append(
                            (part, group, False)
                        )

            previous_end = match.end()

        # Anything after the final group tag
        tail = text[previous_end:].strip(" ,/&+")

        if tail:
            parts = re.split(
                r"\s*(?:,|&|\+|/)\s*",
                tail
            )

            for part in parts:
                part = part.strip(" ,/&+")
                if part:
                    results.append(
                        (part, None, True)
                    )

        if results:
            return results

    # ---------------------------------------------------------
    # CASE 2: Multiple faculty without groups
    # ---------------------------------------------------------
    #
    # Separators:
    #   &
    #   and
    #   /
    #   comma
    #   +
    #
    parts = re.split(
        r"\s*(?:,|&|\band\b|/|\+)\s*",
        text,
        flags=re.IGNORECASE,
    )

    parts = [
        p.strip(" ,/&+")
        for p in parts
        if p.strip(" ,/&+")
    ]

    # No meaningful split
    if len(parts) == 1:
        return [(parts[0], None, False)]

    # Clearly multiple faculty
    if 1 < len(parts) <= 6:
        return [
            (part, None, False)
            for part in parts
        ]

    # Safety fallback:
    # Never invent faculty identities.
    return [(text, None, True)]