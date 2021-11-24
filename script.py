import argparse
import docker
import time
from concurrent.futures import ThreadPoolExecutor

INPUT_FILENAME = 'input.txt'
IMAGE_NAME = 'parallel-example'
DATA = []

with open(INPUT_FILENAME) as file:
    DATA = [' '.join(line.strip().split(',')) for line in file.readlines()]


def run_container(numbers, start, client):
    container = client.containers.run(
        image = IMAGE_NAME,
        command=f'sh ./mean.sh {numbers}',
        detach=True
    )
    time_from_start = time.time() - start
    logs = str(container.logs(), encoding='utf-8').strip('-\n')

    print(f'Time: {time_from_start: .2f} {container.name : <30} {logs : <30}')


def single_thread():
    client = docker.from_env()
    start = time.time()
    for numbers in DATA:
        run_container(numbers, start, client)


def multi_thread(n_threads):
    client = docker.from_env()
    with ThreadPoolExecutor(n_threads) as pool:
        start = time.time()
        for numbers in DATA:
             pool.submit(run_container, numbers, start, client)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', '-t', help='number of threads', type=int, default=1)
    args = parser.parse_args()
    if args.threads == 1:
        single_thread()
    else:
        multi_thread(args.threads)
