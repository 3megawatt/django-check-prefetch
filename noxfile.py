import nox

nox.options.stop_on_first_error = True

source_files = ("check_prefetch", "tests/app", "noxfile.py")


@nox.session(reuse_venv=True)
def check(session):
    session.install("black", "flake8", "flake8-bugbear", "flake8-comprehensions")

    session.run("black", "--check", "--diff", *source_files)
    session.run("flake8", *source_files)


@nox.session(reuse_venv=True)
@nox.parametrize("django", ["2.2", "3.0"])
def test(session, django):
    session.install(f"django=={django}")
    session.run("make", "test")
