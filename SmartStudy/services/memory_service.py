
from database.db_manager import (
    save_learning_interaction,
    get_learning_history,
)


VALID_INTERACTION_TYPES = {
    "general_question",
    "document_question",
    "quiz",
}


def record_learning_activity(
    interaction_type,
    topic,
    content,
    score=None,
):
    """
    Validate and save a student learning interaction.
    """

    if interaction_type not in VALID_INTERACTION_TYPES:
        raise ValueError("Invalid learning interaction type.")

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic must be a non-empty string.")

    if not isinstance(content, str) or not content.strip():
        raise ValueError("Content must be a non-empty string.")

    if score is not None:
        if type(score) is not int or score not in (0, 1):
            raise ValueError("Quiz score must be 0 or 1.")

    if interaction_type != "quiz" and score is not None:
        raise ValueError(
            "Only quiz interactions can have a score."
        )

    return save_learning_interaction(
        interaction_type=interaction_type,
        topic=topic.strip(),
        content=content.strip(),
        score=score,
    )


def retrieve_learning_history(limit=10):
    """
    Retrieve recent student learning interactions.
    """

    if type(limit) is not int or limit <= 0:
        raise ValueError(
            "History limit must be a positive integer."
        )

    return get_learning_history(limit=limit)
