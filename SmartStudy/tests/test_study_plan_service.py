
# ---------------------------------------------------------
# SmartStudy - Study Planning Service Tests
# Phase 11: Automated Scheduling Validation
# ---------------------------------------------------------

import unittest

from services.study_plan_service import (
    allocate_study_time,
    generate_study_sessions,
    generate_study_schedule,
)


class TestStudyPlanService(unittest.TestCase):

    def setUp(self):
        self.topics = [
            {"topic": "Primary Keys", "classification": "Developing"},
            {"topic": "Foreign Keys", "classification": "Weak"},
            {"topic": "SQL Joins", "classification": "Strong"},
        ]

    def test_study_time_allocation(self):
        plan = allocate_study_time(self.topics, 70)

        self.assertEqual(
            sum(item["allocated_minutes"] for item in plan),
            70,
        )

        # Weak topics should receive more time than strong topics.
        allocations = {
            item["topic"]: item["allocated_minutes"]
            for item in plan
        }

        self.assertGreater(
            allocations["Foreign Keys"],
            allocations["SQL Joins"],
        )

    def test_study_session_generation(self):
        plan = allocate_study_time(self.topics, 70)
        sessions = generate_study_sessions(plan)

        self.assertEqual(len(sessions), 3)

        for session in sessions:
            self.assertGreater(session["duration_minutes"], 0)
            self.assertTrue(session["activity"])

    def test_balanced_daily_schedule(self):
        sessions = [
            {
                "topic": "Primary Keys",
                "classification": "Developing",
                "duration_minutes": 281,
                "activity": "Revision",
            },
            {
                "topic": "Foreign Keys",
                "classification": "Insufficient Data",
                "duration_minutes": 188,
                "activity": "Practice",
            },
        ]

        schedule = generate_study_schedule(
            sessions,
            number_of_days=7,
        )

        self.assertEqual(len(schedule), 7)

        for day in schedule:
            self.assertEqual(day["total_minutes"], 67)

        self.assertEqual(
            sum(day["total_minutes"] for day in schedule),
            469,
        )

        # Verify each topic retains its original allocation.
        topic_totals = {}

        for day in schedule:
            for session in day["sessions"]:
                topic = session["topic"]

                topic_totals[topic] = (
                    topic_totals.get(topic, 0)
                    + session["duration_minutes"]
                )

        self.assertEqual(topic_totals["Primary Keys"], 281)
        self.assertEqual(topic_totals["Foreign Keys"], 188)

    def test_invalid_study_duration(self):
        with self.assertRaises(ValueError):
            allocate_study_time(self.topics, 0)

        with self.assertRaises(ValueError):
            allocate_study_time(self.topics, -10)

    def test_invalid_number_of_days(self):
        with self.assertRaises(ValueError):
            generate_study_schedule([], 0)

        with self.assertRaises(ValueError):
            generate_study_schedule([], -1)

    def test_empty_study_sessions(self):
        schedule = generate_study_schedule([], 3)

        self.assertEqual(len(schedule), 3)

        for day in schedule:
            self.assertEqual(day["total_minutes"], 0)
            self.assertEqual(day["sessions"], [])


    def test_more_topics_than_available_minutes(self):
        topics = [
            {"topic": f"Topic {i}", "classification": "Weak"}
            for i in range(5)
        ]

        plan = allocate_study_time(topics, 2)

        self.assertEqual(
            sum(item["allocated_minutes"] for item in plan),
            2,
        )

        self.assertEqual(
            sum(item["allocated_minutes"] > 0 for item in plan),
            2,
        )

    def test_invalid_session_duration(self):
        sessions = [
            {
                "topic": "Primary Keys",
                "classification": "Developing",
                "duration_minutes": -5,
                "activity": "Revision",
            }
        ]

        with self.assertRaises(ValueError):
            generate_study_schedule(sessions, 3)

    def test_uneven_daily_time_distribution(self):
        sessions = [
            {
                "topic": "Primary Keys",
                "classification": "Developing",
                "duration_minutes": 5,
                "activity": "Revision",
            },
            {
                "topic": "Foreign Keys",
                "classification": "Weak",
                "duration_minutes": 5,
                "activity": "Practice",
            },
        ]

        schedule = generate_study_schedule(sessions, 3)

        daily_totals = [
            day["total_minutes"]
            for day in schedule
        ]

        self.assertEqual(sum(daily_totals), 10)

        # Daily totals must differ by no more than one minute.
        self.assertLessEqual(
            max(daily_totals) - min(daily_totals),
            1,
        )


if __name__ == "__main__":
    unittest.main()
