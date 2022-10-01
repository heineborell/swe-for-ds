"""example of using threads and processes at the same time

to get timing, invoke from the terminal as

    time python preprocess_data --processes 2 --threads 4 --num-datapoints 1024
"""
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial

import pandas as pd

from someproject.data_processing import DataStore, compute_important_value


def get_data(data_ids: list[int]) -> list[int]:
    """get data from the "external" data store -- I/O bounded

    Takes 1 second for every 10 data points retrieved

    """
    datastore = DataStore(database="fakedb")
    return [datastore.get_data(i) for i in data_ids]


def process_batch(data_ids: list[int], threads: int) -> float:
    """each batch will use threads to get data then process"""

    # I/O bounded getting of data per process
    batch_size = int(len(data_ids) / threads)
    data_id_batches = [
        data_ids[i : i + batch_size] for i in range(0, len(data_ids), batch_size)
    ]
    with ThreadPoolExecutor(max_workers=threads) as t_exec:
        retrieved_batches = list(t_exec.map(get_data, data_id_batches))

    # perform the compute bounded operations here
    # compute_important_value takes 1 second per every 100 datapoints
    data_single_list = [datum for batch in retrieved_batches for datum in batch]
    return compute_important_value(data_single_list)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--processes", "-p", type=int, default=1)
    parser.add_argument("--threads", "-t", type=int, default=1)
    parser.add_argument("--num-datapoints", "-n", type=int, default=1024)
    args = parser.parse_args()

    # first we have a bunch of data ids we need to process
    data_ids = list(range(args.num_datapoints))

    # split the IDs into batches, one batch per process
    batch_size = int(args.num_datapoints / args.processes)
    data_id_batches = [
        data_ids[i : i + batch_size] for i in range(0, args.num_datapoints, batch_size)
    ]

    process_batch_partial = partial(process_batch, threads=args.threads)
    with ProcessPoolExecutor(max_workers=args.processes) as p_exec:
        processed_batches = list(p_exec.map(process_batch_partial, data_id_batches))

    # re-aggregate data
    data = [datum for batch in processed_batches for datum in batch]
    df = pd.DataFrame({"value": data})

    # save for future use
    df.to_csv("data.csv", index=False)
