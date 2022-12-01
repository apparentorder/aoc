import os
import re
import subprocess

import requests
import time
import webbrowser
from bs4 import BeautifulSoup
from tools.datafiles import JSONFile
from tools.stopwatch import StopWatch
from typing import Any, Callable, List, Tuple, Type, Union
from .tools import get_script_dir

BASE_PATH = get_script_dir()
INPUTS_PATH = os.path.join(BASE_PATH, 'inputs')


class AOCDay:
    year: int
    day: int
    input: List[str]  # our input is always a list of str/lines
    inputs: List[List[Tuple[Any, str]]]
    part_func: List[Callable]

    def __init__(self, year: int, day: int):
        self.day = day
        self.year = year
        self.part_func = [self.part1, self.part2]

    def part1(self) -> Any:
        raise NotImplementedError()

    def part2(self) -> Any:
        raise NotImplementedError()

    def run_part(self, part: int, verbose: bool = False, measure_runtime: bool = False, timeit_number: int = 50):
        case_count = 0
        for solution, input_file in self.inputs[part]:
            exec_time = None
            answer = None
            self._load_input(input_file)

            if not measure_runtime or case_count < len(self.inputs[part]) - 1:
                answer = self.part_func[part]()
            else:
                stopwatch = StopWatch()
                for _ in range(timeit_number):
                    answer = self.part_func[part]()
                stopwatch.stop()
                exec_time = stopwatch.avg_string(timeit_number)

            if solution is None:
                print_solution(self.day, part + 1, answer, solution, case_count, exec_time)
                if answer not in {u"", b"", None, b"None", u"None"}:
                    self._submit(part + 1, answer)
            else:
                if verbose or answer != solution:
                    print_solution(self.day, part + 1, answer, solution, case_count, exec_time)

                if answer != solution:
                    return False

            case_count += 1
            if case_count == len(self.inputs[part]) and not verbose:
                print_solution(self.day, part + 1, answer, exec_time=exec_time)

    def run(self, parts: int = 3, verbose: bool = False, measure_runtime: bool = False, timeit_number: int = 50):
        if parts & 1:
            self.run_part(0, verbose, measure_runtime, timeit_number)
        if parts & 2:
            self.run_part(1, verbose, measure_runtime, timeit_number)

    def _load_input(self, filename):
        file_path = os.path.join(INPUTS_PATH, filename)
        if not os.path.exists(file_path):
            self._download_input(file_path)

        with open(os.path.join(INPUTS_PATH, filename)) as f:
            self.input = f.read().splitlines()

    def _download_input(self, filename: str):
        # FIXME: implement wait time for current day before 06:00:00 ?
        session_id = open(".session", "r").readlines()[0].strip()
        response = requests.get(
            "https://adventofcode.com/%d/day/%d/input" % (self.year, self.day),
            cookies={'session': session_id}
        )
        if not response.ok:
            print("FAILED to download input: (%s) %s" % (response.status_code, response.text))
            return

        with open(filename, "wb") as f:
            f.write(response.content)
            f.flush()

        if os.path.exists(".git"):
            subprocess.call(["git", "add", filename])

    def _submit(self, part: int, answer: Any):
        answer_cache = JSONFile("answer_cache.json", create=True)
        str_day = str(self.day)
        str_part = str(part)
        if str_day not in answer_cache:
            answer_cache[str_day] = {}

        if str_part not in answer_cache[str_day]:
            answer_cache[str_day][str_part] = {
                'wrong': [],
                'correct': None
            }

        if answer in answer_cache[str_day][str_part]['wrong']:
            print("Already tried %s. It was WRONG." % answer)
            return

        if answer_cache[str_day][str_part]['correct'] is not None:
            if answer == answer_cache[str_day][str_part]['correct']:
                print("Already submitted %s. It was CORRECT." % answer)
                return
            else:
                print("Already submitted an answer, but another one")
                print("CORRECT was: %s" % answer_cache[str_day][str_part]['correct'])
                print("Your answer: %s" % answer)
                return

        print("Submitting %s as answer for %d part %d" % (answer, self.day, part))
        session_id = open(".session", "r").readlines()[0].strip()
        response = requests.post(
            "https://adventofcode.com/%d/day/%d/answer" % (self.year, self.day),
            cookies={'session': session_id},
            data={'level': part, 'answer': answer}
        )

        if not response.ok:
            print("Failed to submit answer: (%s) %s" % (response.status_code, response.text))

        soup = BeautifulSoup(response.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            answer_cache[str_day][str_part]['correct'] = answer
            print("That's correct!")
            webbrowser.open("https://adventofcode.com/%d/day/%d#part2" % (self.year, self.day))
        elif "That's not the right answer" in message:
            answer_cache[str_day][str_part]['wrong'].append(answer)
            print("That's WRONG!")
        elif "You gave an answer too recently" in message:
            # WAIT and retry
            wait_pattern = r"You have (?:(\d+)m )?(\d+)s left to wait"
            try:
                [(minutes, seconds)] = re.findall(wait_pattern, message)
            except ValueError:
                print("wait_pattern unable to find wait_time in:")
                print(message)
                return

            seconds = int(seconds)
            if minutes:
                seconds *= int(minutes) * 60

            print("TOO SOON. Waiting %d seconds until auto-retry." % seconds)
            time.sleep(seconds)
            self._submit(part, answer)
            return
        else:
            print("I don't know what this means:")
            print(message)
            return

        answer_cache.save()

    def getInput(self) -> Union[str, List]:
        if len(self.input) == 1:
            return self.input[0]
        else:
            return self.input.copy()

    def getInputListAsType(self, return_type: Type) -> List:
        """
        get input as list casted to return_type, each line representing one list entry
        """
        return [return_type(i) for i in self.input]

    def getMultiLineInputAsArray(self, return_type: Type = None, join_char: str = None) -> List:
        """
        get input for day x as 2d array, split by empty lines
        """
        lines = self.input.copy()
        lines.append('')

        return_array = []
        line_array = []
        for line in lines:
            if not line:
                if join_char:
                    return_array.append(join_char.join(line_array))
                else:
                    return_array.append(line_array)
                line_array = []
                continue

            if return_type:
                line_array.append(return_type(line))
            else:
                line_array.append(line)

        return return_array

    def getInputAsArraySplit(self, split_char: str = ',', return_type: Union[Type, List[Type]] = None) -> List:
        """
        get input for day x with the lines split by split_char
        if input has only one line, returns a 1d array with the values
        if input has multiple lines, returns a 2d array (a[line][values])
        """
        if len(self.input) == 1:
            return split_line(line=self.input[0], split_char=split_char, return_type=return_type)
        else:
            return_array = []
            for line in self.input:
                return_array.append(split_line(line=line, split_char=split_char, return_type=return_type))

            return return_array


def print_solution(day: int, part: int, solution: Any, test: Any = None, test_case: int = 0, exec_time: str = None):
    if test is not None:
        print(
            "%s (TEST day%d/part%d/case%d): got '%s'; expected '%s'"
            % ("OK" if test == solution else "FAIL", day, part, test_case, solution, test)
        )
    else:
        print(
            "Solution to day %s, part %s: %s"
            % (
                day,
                part,
                solution,
            )
        )

    if exec_time:
        print("Day %s, Part %s - Average run time: %s" % (day, part, exec_time))


def split_line(line, split_char: str = ',', return_type: Union[Type, List[Type]] = None):
    if split_char:
        line = line.split(split_char)

    if return_type is None:
        return line
    elif isinstance(return_type, list):
        return [return_type[x](i) if len(return_type) > x else i for x, i in enumerate(line)]
    else:
        return [return_type(i) for i in line]
