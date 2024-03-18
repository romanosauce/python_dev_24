import cowsay
import asyncio

clients = {}                        # cow name to client_id
clients_queue = {}                  # client_id to client_queue
clients_cows = {}                   # client_id to cow


async def chat(reader, writer):
    client_id = "{}:{}".format(*writer.get_extra_info('peername'))
    clients_queue[client_id] = asyncio.Queue()
    receive_data_from_client = asyncio.create_task(reader.readline())
    write_data_to_client = asyncio.create_task(clients_queue[client_id].get())
    print(f"New connection from {client_id}")
    writer.write('>>> '.encode())
    await writer.drain()

    while not reader.at_eof():
        done, pending = await asyncio.wait([receive_data_from_client, write_data_to_client],
                                           return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is receive_data_from_client:
                receive_data_from_client = asyncio.create_task(reader.readline())
                data = q.result().decode().strip()
                data = data.split()
                match data:
                    case ['who']:
                        writer.write((' '.join(clients.keys()) + '\n>>> ').encode())
                    case ['cows']:
                        writer.write((' '.join(cow for cow in cowsay.list_cows()
                                               if cow not in clients) + '\n>>> ').encode())
                    case ['login', cow]:
                        if cow not in clients and cow in cowsay.list_cows():
                            clients[cow] = client_id
                            clients_cows[client_id] = cow
                            writer.write('>>> '.encode())
                        else:
                            writer.write('invalid cow\n>>> '.encode())
                    case ['say', cow, *text]:
                        if client_id in clients_cows:
                            if cow in clients:
                                if text:
                                    msg = '\n' + cowsay.cowsay(' '.join(text), cow=clients_cows[client_id])
                                    await clients_queue[clients[cow]].put(msg)
                                    writer.write('>>> '.encode())
                                else:
                                    writer.write('invalid message\n>>> '.encode())
                            else:
                                writer.write('invalid cow\n>>> '.encode())
                        else:
                            writer.write("you can't send messages\nPlease log in\n>>> ".encode())
                    case ['yield', *text]:
                        if client_id in clients_cows:
                            for id in clients_cows:
                                if id != client_id :
                                    queue = clients_queue[id]
                                    msg = '\n' + cowsay.cowsay(' '.join(text), cow=clients_cows[client_id])
                                    await queue.put(msg)
                            writer.write(">>> ".encode())
                        else:
                            writer.write("you can't send messages\nPlease log in\n>>> ".encode())
                    case ['quit']:
                        print(f"We lost {client_id}")
                        receive_data_from_client.cancel()
                        write_data_to_client.cancel()
                        del clients_queue[client_id]
                        client_cow = clients_cows[client_id]
                        del clients_cows[client_id]
                        del clients[client_cow]
                        writer.close()
                        await writer.wait_closed()
                        return
                    case _:
                        writer.write("unknown command\n>>> ".encode())
            elif q is write_data_to_client:
                write_data_to_client = asyncio.create_task(clients_queue[client_id].get())
                data = q.result()
                writer.write((data + '\n>>> ').encode())
            await writer.drain()
    print(f"We lost {client_id}")
    receive_data_from_client.cancel()
    write_data_to_client.cancel()
    del clients_queue[client_id]
    client_cow = clients_cows[client_id]
    del clients_cows[client_id]
    del clients[client_cow]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
