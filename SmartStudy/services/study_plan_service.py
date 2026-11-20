
# ---------------------------------------------------------
# SmartStudy - Study Planning Service
# Phase 11: AI-Powered Study Planning
# ---------------------------------------------------------

# Priority weights for each learning classification.
# Higher weights mean more study time.
STUDY_PRIORITY_WEIGHTS = {
    "Weak": 4,
    "Developing": 3,
    "Insufficient Data": 2,
    "Strong": 1,
}


def allocate_study_time(topic_assessments, total_minutes):
    """
    Allocate available study time across learning topics.

    Parameters:
        topic_assessments: List of dictionaries containing
            topic and classification information.
        total_minutes: Total available study time.

    Returns:
        A list of dictionaries containing:
            - topic
            - classification
            - allocated_minutes
    """

    if isinstance(total_minutes, bool) or not isinstance(total_minutes, int):
        raise ValueError("Total study time must be an integer.")

    if total_minutes <= 0:
        raise ValueError("Total study time must be greater than zero.")

    if not topic_assessments:
        return []

    weights = []

    for assessment in topic_assessments:
        classification = assessment["classification"]

        if classification not in STUDY_PRIORITY_WEIGHTS:
            raise ValueError(
                f"Unknown learning classification: {classification}"
            )

        weights.append(STUDY_PRIORITY_WEIGHTS[classification])

    total_weight = sum(weights)

    # Calculate each topic's exact proportional allocation.
    exact_minutes = [
        total_minutes * weight / total_weight
        for weight in weights
    ]

    # Allocate whole minutes first.
    allocated_minutes = [
        int(minutes) for minutes in exact_minutes
    ]

    # Distribute any remaining minutes to topics with
    # the largest fractional remainders.
    remaining_minutes = total_minutes - sum(allocated_minutes)

    remainder_order = sorted(
        range(len(exact_minutes)),
        key=lambda index: (
            -(exact_minutes[index] - allocated_minutes[index]),
            -weights[index],
            index,
        ),
    )

    for index in remainder_order[:remaining_minutes]:
        allocated_minutes[index] += 1

    study_plan = []

    for assessment, minutes in zip(
        topic_assessments, allocated_minutes
    ):
        study_plan.append({
            "topic": assessment["topic"],
            "classification": assessment["classification"],
            "allocated_minutes": minutes,
        })

    return study_plan


def generate_study_sessions(study_plan):
    """
    Generate personalized study sessions based on
    each topic's learning classification.

    Parameters:
        study_plan: List of dictionaries containing:
            - topic
            - classification
            - allocated_minutes

    Returns:
        A list of study sessions with recommended activities.
    """

    activity_mapping = {
        "Weak": "Review basic concepts and practice easy quizzes",
        "Developing": "Revise key concepts and attempt medium quizzes",
        "Insufficient Data": "Study the topic and complete an initial quiz",
        "Strong": "Review advanced concepts and attempt hard quizzes",
    }

    study_sessions = []

    for topic_plan in study_plan:
        classification = topic_plan["classification"]
        allocated_minutes = topic_plan["allocated_minutes"]

        if classification not in activity_mapping:
            raise ValueError(
                f"Unknown learning classification: {classification}"
            )

        if allocated_minutes <= 0:
            continue

        study_sessions.append({
            "topic": topic_plan["topic"],
            "classification": classification,
            "duration_minutes": allocated_minutes,
            "activity": activity_mapping[classification],
        })

    return study_sessions
