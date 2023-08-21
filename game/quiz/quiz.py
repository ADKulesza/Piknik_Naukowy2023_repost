import csv
import time
from pathlib import Path
from random import shuffle

import pygame

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier
from common.base_game import BaseGame
from common.components.animation import Animation
from game.quiz.answer import Answer
from game.quiz.question import Question


class Quiz(BaseGame):
    name = "Quiz"

    def __init__(self):
        super().__init__()
        self.question_pool = None
        self.load_questions()

        self.number_of_questions = 100

    def load_questions(self):
        with open(Path(__file__).parent / "questions.csv") as f:
            reader = csv.DictReader(f)
            questions = [q for q in reader]

        question_pool = []

        for question in questions:
            question_dict = {}
            question_dict["difficulty"] = 1
            question_dict["question"] = question.pop("Pytanie")
            correct = question.pop("Prawidłowa odp").upper()
            answers = dict()
            answers["correct"] = question.pop(correct)
            answers["other"] = [q for q in question.values()]
            question_dict["answers"] = answers

            question_pool.append(question_dict)

        self.question_pool = question_pool

    def get_questions(self, difficulty):
        question_pool = [
            question
            for question in self.question_pool
            if question["difficulty"] == difficulty
        ]

        # shuffle(question_pool)
        return question_pool[: self.number_of_questions]

    def run(self):
        from common.components.core.app import App

        app = App()
        screen = app.canvas

        answers_positions = [
            (app.canvas.get_width() / 3, 450),
            (2 * app.canvas.get_width() / 3, 450),
            (app.canvas.get_width() / 3, 600),
            (2 * app.canvas.get_width() / 3, 600),
        ]

        font_name = app.theme.font_name
        font_size = 30
        font = pygame.font.Font(font_name, font_size)

        in_game = True

        difficulty = 1
        questions = self.get_questions(difficulty)

        level = 1

        background = Animation(
            Path(__file__).parent / "assets/background", dimensions=screen.get_size()
        )

        time_delay_seconds = 1
        time_delay_ms = time_delay_seconds * 1000
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, time_delay_ms)

        while questions and in_game:
            question = questions.pop(0)

            question_content = question["question"]
            correct_answer = question["answers"]["correct"]
            other_answers = question["answers"]["other"]

            answers = [correct_answer, *other_answers]
            shuffle(answers)
            answers = [Answer(answer) for answer in answers]

            for pos, answer in zip(answers_positions, answers):
                answer.rect.center = pos

            answers_idx = 0

            selected_answer = None

            question_number_text = (
                f"Pozostało jeszcze {self.number_of_questions - level + 1} pytań"
            )
            question_number_image = font.render(
                question_number_text, True, app.theme.primary_color
            )
            question_number_rect = question_number_image.get_rect()
            question_number_rect.center = (screen.get_width() // 2, 50)

            question = Question(question_content)
            question.rect.center = screen.get_width() // 2, 200

            protection_time_ticks = 1
            protection_ticks = 0

            protection = True

            while selected_answer is None:
                if protection:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                return
                        if event.type == pygame.QUIT:
                            return
                        elif event.type == timer_event:
                            protection_ticks += 1
                    if protection_ticks == protection_time_ticks:
                        protection = False

                if not protection:
                    for i, answer in enumerate(answers):
                        if i == answers_idx:
                            answer.highlight("SILVER")
                        else:
                            answer.unhighlight()

                    if not isinstance(app.amplifier.amp, DummyAmplfier):
                        if app.get_emg_value() > app.player.mean:
                            selected_answer = answers_idx

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                selected_answer = answers_idx
                            if event.key == pygame.K_p:
                                return
                        if event.type == pygame.QUIT:
                            return
                        elif event.type == timer_event:
                            answers_idx += 1
                            answers_idx %= len(answers)

                screen.fill("BLACK")
                background.update(screen)

                question.update(screen)
                screen.blit(question_number_image, question_number_rect)

                if selected_answer is not None:
                    print(answers[selected_answer].text)
                    for answer in answers:
                        answer.unhighlight()

                    if answers[selected_answer].text == correct_answer:
                        level += 1
                        answers[selected_answer].highlight("GREEN")
                    else:
                        in_game = False
                        answers[selected_answer].highlight("RED")

                for answer in answers:
                    answer.update(screen)
                pygame.display.update()
                app.tick()
            pygame.display.update()
            app.tick()
            time.sleep(time_delay_seconds)
            pygame.event.get()

        if level == self.number_of_questions:
            print("wygrana")
        else:
            print("No prawie")
