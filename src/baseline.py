def heuristic_estimate(story: str) -> int:
    """
    A simple keyword-based heuristic for story point estimation.
    This is a baseline method that can be used for comparison.
    """
    # Define complexity indicators
    low_complexity_indicators = ["view", "read", "list", "display", "browse"]
    medium_complexity_indicators = ["update", "create", "form", "auth",
        "discount", "assign"]
    high_complexity_indicators = ["integrate", "export", "import", "payment",
        "real time", "dashboard", "analytics",
        "notifications"]

    story_lower = story.lower()

    # Count complexity indicators
    low_count = sum(1 for indicator in low_complexity_indicators
                    if indicator in story_lower)
    medium_count = sum(1 for indicator in medium_complexity_indicators
                       if indicator in story_lower)
    high_count = sum(1 for indicator in high_complexity_indicators
                     if indicator in story_lower)

    # Determine score based on complexity indicators
    if high_count > 0:
        return min(10, 6 + high_count)  # High complexity: 6-10 points
    elif medium_count > 0:
        return min(8, 3 + medium_count)  # Medium complexity: 3-8 points
    elif low_count > 0:
        return min(5, 1 + low_count)  # Low complexity: 1-5 points
    else:
        return 3  # Default for unrecognized patterns

