import os
import tempfile
from tempfile import NamedTemporaryFile

from src.decorators import log


def test_log_success_console(capsys):

    @log()
    def success_func():
        return 42

    result = success_func()
    assert result == 42

    captured = capsys.readouterr()
    assert "success_func ok" in captured.out
    assert captured.err == ""


def test_log_exception_console(capsys):
    @log()
    def error_func():
        raise ValueError("test error")

    try:
        error_func()
    except ValueError:
        pass

    captured = capsys.readouterr()
    assert "error_func error ValueError" in captured.out
    assert "test error" in captured.out
    assert captured.err == ""


def test_log_to_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".log") as tmp:
        filename = tmp.name

    try:

        @log(filename=filename)
        def file_func():
            return "done"

        result = file_func()
        assert result == "done"

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        assert "file_func ok" in content
    finally:
        os.unlink(filename)


def test_log_exception_to_file():

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".log") as tmp:
        filename = tmp.name

    try:

        @log(filename=filename)
        def file_error_func():
            raise RuntimeError("file error")

        try:
            file_error_func()
        except RuntimeError:
            pass

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        assert "file_error_func error RuntimeError" in content
        assert "file error" in content
    finally:
        os.unlink(filename)


def test_log_no_console_output_when_writing_to_file(capsys):

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".log") as tmp:
        filename = tmp.name

    try:

        @log(filename=filename)
        def silent_func():
            return "silent"

        silent_func()

        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""
    finally:
        os.unlink(filename)


def test_log_to_console(capsys):
    """Проверяет базовую функциональность декоратора, когда файл записи не указан (по умолчанию filename=None)."""

    @log()
    def func_with_args(a, b=42):
        return a + b

    result = func_with_args(5)

    assert result == 47

    captured = capsys.readouterr()

    expected_in_stdout = "func_with_args ok"
    assert expected_in_stdout in captured.out.strip()


def test_log_to_file():
    """Проверяет, что при указании файла лог пишется ТОЛЬКО в него."""

    with NamedTemporaryFile(mode="w+", delete=False, suffix=".log") as tmp:

        @log(filename=tmp.name)
        def func_with_args(a, b=42):
            return a + b

        func_with_args(5)

        with open(tmp.name, encoding="utf-8") as f:
            content = f.read().strip()

        expected_in_file = "func_with_args ok"
        assert expected_in_file in content


def test_error_to_console(capsys):
    """Проверяет, что при ошибке в функции в консоль выводится информация об исключении."""

    @log()
    def error_func():
        raise ValueError("Test error")

    try:
        error_func()
    except Exception:
        pass

    captured = capsys.readouterr()

    expected_in_stdout = "error_func error ValueError: Test error"
    assert expected_in_stdout in captured.out.strip()
