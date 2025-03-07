from __future__ import annotations

import typing

import flood


def generate_test_eth_get_logs(
    *,
    rates: typing.Sequence[int],
    network: str,
    duration: int | None = None,
    durations: typing.Sequence[int] | None = None,
    vegeta_kwargs: typing.Mapping[str, str | None] | None = None,
    random_seed: flood.RandomSeed | None = None,
) -> flood.LoadTest:
    n_calls = flood.estimate_call_count(
        rates=rates, duration=duration, durations=durations
    )
    calls = flood.generate_calls_eth_get_logs_no_filter(
        n_calls,
        network=network,
        random_seed=random_seed,
    )
    return flood.create_load_test(
        calls=calls,
        rates=rates,
        duration=duration,
        durations=durations,
    )


# def generate_tests_eth_get_logs_by_contract(
#     url: str,
#     rates: typing.Sequence[int],
#     duration: int,
#     range_size: int,
# ) -> typing.Mapping[str, flood.LoadTest]:
#     """test: Transfers of USDC vs DAI vs LUSD"""

#     n_calls = flood.estimate_call_count(rates=rates, duration=duration)

#     block_ranges = flood.generate_block_ranges(
#         start_block=12_178_594,
#         end_block=17_000_000,
#         n=n_calls,
#         range_size=range_size,
#     )

#     tests: typing.MutableMapping[str, flood.LoadTest] = {}
#     for name, contract_address in contracts.items():
#         calls = flood.generate_calls_eth_get_logs(
#             contract_address=contract_address,
#             topics=[event_hashes['Transfer']],
#             block_ranges=block_ranges,
#         )
#         tests[name] = {
#             'url': url,
#             'rates': rates,
#             'duration': duration,
#             'calls': calls,
#         }

#     return tests


# def generate_tests_eth_get_logs_by_block_range_size(
#     url: str,
#     rates: typing.Sequence[int],
#     duration: int,
#     range_sizes: typing.Sequence[int],
# ) -> typing.Mapping[str, flood.LoadTest]:
#     """test: tiny vs small vs medium vs large block ranges"""

#     n_calls = flood.estimate_call_count(rates=rates, duration=duration)

#     tests: typing.MutableMapping[str, flood.LoadTest] = {}
#     for range_size in range_sizes:
#         block_ranges = flood.generate_block_ranges(
#             start_block=12_178_594,
#             end_block=17_000_000,
#             n=n_calls,
#             range_size=range_size,
#         )
#         calls = flood.generate_calls_eth_get_logs(
#             contract_address=contracts['USDC'],
#             topics=[event_hashes['Transfer']],
#             block_ranges=block_ranges,
#         )
#         name = str(range_size) + '_blocks'
#         tests[name] = {
#             'url': url,
#             'rates': rates,
#             'duration': duration,
#             'calls': calls,
#         }

#     return tests


# def generate_tests_eth_get_logs_by_block_age(
#     url: str,
#     rates: typing.Sequence[int],
#     duration: int,
#     block_bounds: typing.Mapping[str, tuple[int, int]],
# ) -> typing.Mapping[str, flood.LoadTest]:
#     """test old vs new blocks"""

#     n_calls = flood.estimate_call_count(rates=rates, duration=duration)

#     tests: typing.MutableMapping[str, flood.LoadTest] = {}
#     for name, (start_block, end_block) in block_bounds.items():
#         block_ranges = flood.generate_block_ranges(
#             start_block=start_block,
#             end_block=end_block,
#             n=n_calls,
#             range_size=100,
#         )
#         calls = flood.generate_calls_eth_get_logs(
#             contract_address=contracts['USDC'],
#             topics=[event_hashes['Transfer']],
#             block_ranges=block_ranges,
#         )
#         tests[name] = {
#             'url': url,
#             'rates': rates,
#             'duration': duration,
#             'calls': calls,
#         }

#     return tests
