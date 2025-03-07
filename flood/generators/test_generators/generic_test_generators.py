from __future__ import annotations

import typing

import flood


#
# # bookkeeping
#


def get_single_test_generators() -> (
    typing.Mapping[str, flood.LoadTestGenerator]
):
    return {
        get_test_generator_display_name(item): item  # type: ignore
        for item in dir(flood)
        if item.startswith('generate_test_')
    }


def get_multi_test_generators() -> (
    typing.Mapping[str, flood.MultiLoadTestGenerator]
):
    return {
        get_test_generator_display_name(item, multi=True): item  # type: ignore
        for item in dir(flood)
        if item.startswith('generate_tests_')
    }


def get_test_generator(test_name: str) -> flood.LoadTestGenerator:
    function_name = get_test_generator_function_name(test_name)
    if hasattr(flood, function_name):
        return getattr(flood, function_name)  # type: ignore
    else:
        raise Exception()


def get_tests_generator(test_name: str) -> flood.MultiLoadTestGenerator:
    function_name = get_test_generator_function_name(test_name)
    if hasattr(flood, function_name):
        return getattr(flood, function_name)  # type: ignore
    else:
        raise Exception()


def get_test_generator_display_name(
    test: str | flood.LoadTestGenerator,
    multi: bool = False,
) -> str:
    if multi:
        prefix = 'generate_tests_'
    else:
        prefix = 'generate_test_'

    if not isinstance(test, str):
        import types

        if not isinstance(test, types.FunctionType):
            raise Exception('should be str or function')
        test = test.__name__

    if not test.startswith(prefix):
        raise Exception()
    test = test[len(prefix) :]
    head, tail = test.split('_', 1)
    test = head + '_' + _snake_case_to_camel_case(tail)
    return test


def get_test_generator_function_name(
    display_name: str, multi: bool = False
) -> str:
    if multi:
        prefix = 'generate_tests_'
    else:
        prefix = 'generate_test_'

    function_name = prefix + _camel_case_to_snake_case(display_name)
    return function_name


def _camel_case_to_snake_case(string: str) -> str:
    # adapted from https://stackoverflow.com/a/1176023
    import re

    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def _snake_case_to_camel_case(string: str) -> str:
    pieces = string.split('_')
    return pieces[0] + ''.join(piece.title() for piece in pieces[1:])


#
# # generation
#


def generate_test(
    *,
    test_name: str,
    random_seed: flood.RandomSeed | None = None,
    rates: typing.Sequence[int] | None = None,
    durations: typing.Sequence[int] | None = None,
    vegeta_kwargs: flood.VegetaKwargsShorthand | None = None,
    network: str,
    output_dir: str | None = None,
) -> flood.LoadTest:
    if test_name is None:
        raise Exception('must specify test_name')
    test_generator = get_test_generator(test_name)
    test = test_generator(
        rates=rates,
        durations=durations,
        vegeta_kwargs=vegeta_kwargs,
        network=network,
        random_seed=random_seed,
    )
    if output_dir is not None:
        flood.runners.single_runner.single_runner_io._save_single_run_test(
            test_name=test_name, output_dir=output_dir, test=test
        )
    return test


def generate_tests(
    *,
    test_name: str,
    random_seed: flood.RandomSeed | None = None,
    rates: typing.Sequence[int] | None = None,
    durations: typing.Sequence[int] | None = None,
    vegeta_kwargs: flood.VegetaKwargsShorthand | None = None,
    network: str,
    output_dir: str | None = None,
    common_parameters: typing.Mapping[str, typing.Any] | None = None,
    specific_parameters: typing.Mapping[str, typing.Mapping[str, typing.Any]]
    | None = None,
) -> typing.Mapping[str, flood.LoadTest]:
    if test_name is None:
        raise Exception('must specify test_name')
    test_generator = get_tests_generator(test_name)
    tests = test_generator(
        rates=rates,
        durations=durations,
        vegeta_kwargs=vegeta_kwargs,
        network=network,
        random_seed=random_seed,
        common_parameters=common_parameters,
        specific_parameters=specific_parameters,
    )
    if output_dir is not None:
        flood.runners.multi_runner.multi_runner_io._save_multi_run_tests(
            output_dir=output_dir,
            tests=tests,
        )
    return tests


# def generate_tests(
#     test_name: str,
#     constants: typing.Mapping[str, typing.Any] | None = None,
#     variables: typing.Mapping[
#         str, typing.Mapping[str, typing.Sequence[typing.Any]]
#     ]
#     | None = None,
# ) -> typing.Mapping[str, flood.LoadTest]:
#     """variables is in format {variable_name: {test_name: variable_value}}"""
#     import itertools

#     if constants is None:
#         constants = {}
#     if variables is None:
#         variables = {}

#     # compute input variables
#     tests_kwargs = []
#     combinations = itertools.product(*variables.items())
#     for combination in combinations:
#         test_kwargs = dict(combination, **constants)
#         tests_kwargs.append(test_kwargs)

#     # use test generator function
#     test_generator = get_test_generator(test_name)
#     tests = []
#     for test_kwargs in tests_kwargs:
#         test = test_generator(**test_kwargs)
#         tests.append(test)

#     return tests

