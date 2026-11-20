
# ---------------------------------------------------------
# SmartStudy - Study Planning Service
# Phase 11: AI-Powered Study Planning
# ---------------------------------------------------------

from services.adaptive_learning_service import get_adaptive_quiz_plans

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


def get_personalized_study_plan(total_minutes=60, min_attempts=3):
    """
    Generate a personalized study plan using the student's
    actual quiz performance stored in SQLite.

    Parameters:
        total_minutes: Available study time in minutes.
        min_attempts: Minimum quiz attempts needed for
            a reliable performance classification.

    Returns:
        A list of personalized study sessions.
    """

    # Retrieve topic assessments from learning history.
    topic_assessments = get_adaptive_quiz_plans(
        min_attempts=min_attempts
    )

    # Allocate available study time across topics.
    study_plan = allocate_study_time(
        topic_assessments=topic_assessments,
        total_minutes=total_minutes
    )

    # Generate recommended activities for each topic.
    study_sessions = generate_study_sessions(
        study_plan=study_plan
    )

    return study_sessions


def generate_study_schedule(study_sessions, number_of_days):
    """
    Distribute personalized study sessions evenly across days.

    Each topic retains its total allocated study time,
    while daily study durations remain balanced.
    """

    if isinstance(number_of_days, bool) or not isinstance(number_of_days, int):
        raise ValueError("Number of days must be an integer.")

    if number_of_days <= 0:
        raise ValueError("Number of days must be greater than zero.")

    schedule = [
        {
            "day": day + 1,
            "sessions": [],
            "total_minutes": 0,
        }
        for day in range(number_of_days)
    ]

    for session in study_sessions:
        duration = session["duration_minutes"]

        if isinstance(duration, bool) or not isinstance(duration, int):
            raise ValueError("Session duration must be an integer.")

        if duration < 0:
            raise ValueError("Session duration cannot be negative.")

        # Divide the topic's duration across all study days.
        minutes_per_day, remaining_minutes = divmod(
            duration, number_of_days
        )

        # Assign the base minutes to every day.
        for day_index in range(number_of_days):
            if minutes_per_day > 0:
                daily_session = {
                    **session,
                    "duration_minutes": minutes_per_day,
                }

                schedule[day_index]["sessions"].append(daily_session)
                schedule[day_index]["total_minutes"] += minutes_per_day

        # Distribute leftover minutes to the least busy days.
        for _ in range(remaining_minutes):
            day_index = min(
                range(number_of_days),
                key=lambda index: (
                    schedule[index]["total_minutes"],
                    index,
                ),
            )

            # Find this topic's session for the selected day.
            matching_session = next(
                (
                    item
                    for item in schedule[day_index]["sessions"]
                    if item["topic"] == session["topic"]
                ),
                None,
            )

            if matching_session is not None:
                matching_session["duration_minutes"] += 1
            else:
                daily_session = {
                    **session,
                    "duration_minutes": 1,
                }
                schedule[day_index]["sessions"].append(daily_session)

            schedule[day_index]["total_minutes"] += 1

    return schedule


def get_daily_study_schedule(
    minutes_per_day=60,
    number_of_days=7,
    min_attempts=3
):
    """
    Generate a personalized daily or weekly study schedule
    using the student's actual learning history.

    Parameters:
        minutes_per_day: Available study minutes per day.
        number_of_days: Number of days to schedule.
        min_attempts: Minimum quiz attempts for classification.

    Returns:
        A list of daily study schedules.
    """

    if (
        isinstance(minutes_per_day, bool)
        or not isinstance(minutes_per_day, int)
        or minutes_per_day <= 0
    ):
        raise ValueError(
            "Daily study time must be a positive integer."
        )

    if (
        isinstance(number_of_days, bool)
        or not isinstance(number_of_days, int)
        or number_of_days <= 0
    ):
        raise ValueError(
            "Number of days must be a positive integer."
        )

    # Calculate the total available study time.
    total_minutes = minutes_per_day * number_of_days

    # Generate personalized sessions from SQLite history.
    study_sessions = get_personalized_study_plan(
        total_minutes=total_minutes,
        min_attempts=min_attempts
    )

    # Distribute sessions across the requested days.
    schedule = generate_study_schedule(
        study_sessions=study_sessions,
        number_of_days=number_of_days
    )

    return schedule
