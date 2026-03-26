#!/usr/bin/env python
import sys
import warnings

from ai_software_factory.crew import AiSoftwareFactory

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        'project_idea': (
            'Build a School Attendance Management System. '
            'Features: teacher marks attendance, student attendance dashboard, '
            'monthly attendance reports.'
        )
    }
    try:
        AiSoftwareFactory().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = {
        'project_idea': (
            'Build a School Attendance Management System. '
            'Features: teacher marks attendance, student attendance dashboard, '
            'monthly attendance reports.'
        )
    }
    try:
        AiSoftwareFactory().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        AiSoftwareFactory().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    inputs = {
        'project_idea': (
            'Build a School Attendance Management System. '
            'Features: teacher marks attendance, student attendance dashboard, '
            'monthly attendance reports.'
        )
    }
    try:
        AiSoftwareFactory().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
