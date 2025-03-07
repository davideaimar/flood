from __future__ import annotations

import typing

import flood


def estimate_call_count(
    *,
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    n_repeats: int | None = None,
) -> int:
    if duration is not None:
        n_calls = sum(rate * duration for rate in rates)
    elif durations is not None:
        if len(rates) != len(durations):
            raise Exception('different number of rates vs durations')
        n_calls = sum(
            rate * duration for rate, duration in zip(rates, durations)
        )
    else:
        raise Exception('should specify duration or durations')

    if n_repeats is not None:
        n_calls *= n_repeats

    return n_calls


def create_load_test(
    calls: typing.Sequence[typing.Any],
    rates: typing.Sequence[int],
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    vegeta_kwargs: flood.VegetaKwargs
    | typing.Sequence[flood.VegetaKwargs]
    | None = None,
    repeat_calls: bool = False,
) -> flood.LoadTest:
    # validate inputs
    if len(rates) == 0:
        raise Exception('must specify at least one rate')

    # pluralize singular durations
    if durations is None:
        if duration is None:
            raise Exception('must specify duration or durations')
        durations = [duration] * len(rates)
    assert len(durations) == len(rates)

    # pluralize singular vegeta kwargs
    if vegeta_kwargs is None:
        vegeta_kwargs = {}
    if isinstance(vegeta_kwargs, dict):
        vegeta_kwargs = [vegeta_kwargs] * len(rates)
    if not isinstance(vegeta_kwargs, list):
        raise Exception('invalid input')

    # partition calls into individual attacks
    if not repeat_calls:
        attacks_calls: typing.MutableSequence[typing.Sequence[flood.Call]] = []
        calls_iter = iter(calls)
        for rate, duration in zip(rates, durations):
            n_attack_calls = rate * duration
            attack_calls = []
            for i in range(n_attack_calls):
                attack_calls.append(next(calls_iter))
            attacks_calls.append(attack_calls)
    else:
        attacks_calls = [calls] * len(rates)
    assert len(attacks_calls) == len(rates)

    # create load tests
    load_test: list[flood.VegetaAttack] = []
    for rate, duration, a_calls, attack_kwargs in zip(
        rates, durations, attacks_calls, vegeta_kwargs
    ):
        attack: flood.VegetaAttack = {
            'rate': rate,
            'duration': duration,
            'calls': a_calls,
            'vegeta_kwargs': attack_kwargs,
        }
        load_test.append(attack)

    return load_test
