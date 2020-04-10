"""Script entry point."""
from application import start_bot
from multiprocessing import Process
from config import CHATANGO_ROOMS, CHATANGO_TEST_ROOM, ENVIRONMENT


if __name__ == '__main__':
    if ENVIRONMENT == 'dev':
        start_bot(CHATANGO_ROOMS)
    else:
        processes = []
        for room in CHATANGO_ROOMS:
            p = Process(target=start_bot, args=(room,))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()
