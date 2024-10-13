import socket
import threading
import time
import random

HOST = '127.0.0.1'
PORT = 65432

clients = {}
experiment_running = False
secret_number = None
leaderboard = {}
guessers = 0
started_once = False

def handle_client(conn, addr):
  global clients
  global guessers
  global experiment_running
  global secret_number
  global leaderboard
  global started_once

  client_name = f"{addr[0]}:{addr[1]}"
  if started_once:
    conn.send("Эксперимент уже начался.".encode('utf-8'))
    conn.close()
    return

  clients[client_name] = conn

  print(f"Клиент {client_name} подключился.")

  while True:
    try:
      data = conn.recv(1024).decode('utf-8')
      if data:
        if experiment_running and data.startswith('guess'):
          try:
            data = data[6:]
            guess = int(data)
            if guess == secret_number:
              conn.sendall('You guessed it!'.encode('utf-8'))
              leaderboard[client_name] = leaderboard.get(client_name, 0) + 1
              print(f"Клиент {client_name} угадал число за {leaderboard[client_name]} попыток.")
              guessers += 1
              if (guessers == len(clients)):
                experiment_running = False
                send_all('Experiment finished.', experiment_running)
            elif guess > secret_number:
              leaderboard[client_name] = leaderboard.get(client_name, 0) + 1
              conn.sendall('Too high!'.encode('utf-8'))
            else:
              leaderboard[client_name] = leaderboard.get(client_name, 0) + 1
              conn.sendall('Too low!'.encode('utf-8'))
          except ValueError:
            conn.sendall(f'Invalid input "{data}". Please enter a number after guess.'.encode('utf-8'))
        else:
          conn.sendall('Experiment is not running.'.encode('utf-8'))
      else:
        print(f"Клиент {client_name} отключился.")
        del clients[client_name]
        break
    except ConnectionResetError:
      print(f"Клиент {client_name} отключился.")
      del clients[client_name]
      break

def send_all(message, experiment_running):
  global clients
  for client_name, conn in clients.items():
    try:
      conn.sendall(message.encode('utf-8'))
    except ConnectionResetError:
      print(f"Клиент {client_name} отключился.")
      del clients[client_name]
  if not experiment_running:
    print_leaderboard()

def print_leaderboard():
  global leaderboard
  print("\nТаблица лидеров:")
  for client_name, score in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True):
    print(f"{client_name}: {score} попыток")

def start_experiment():
  global experiment_running
  global secret_number
  global guessers
  global started_once
  guessers = 0
  experiment_running = True
  started_once = True
  send_all('Experiment started!', experiment_running)
  secret_number = random.randint(1, 100)
  print(f"Эксперимент начался. Загаданное число: {secret_number}")

def wait_clients(s):
  while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

def start_server():
  global HOST
  global PORT
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")
    threading.Thread(target=wait_clients, args=(s, )).start()
    print("Введите что-нибудь и эксперимент начнется")
    input()
    if len(clients) == 0:
      print("Никто не пришел")
      s.close()
      exit(0)
    print(f"Подключилось {len(clients)} человек")
    while True:
      command = input("Введите команду (start/leaderboard/clients): ")
      if command == "start":
        start_experiment()
        print(f"Ожидаем ответы от участников: {len(clients)}")
        while abs(len(clients) - guessers) != 0:
          pass
      elif command == "leaderboard":
        print("Таблица лидеров:")
        print_leaderboard()
      elif command == "clients":
        print("Список участников:")
        for client_id in clients.keys():
          print(f"Участник {client_id}")
      elif command == "exit":
        experiment_running = False
        for client in clients.values():
          client.close()
        s.close()
        break


if __name__ == '__main__':
  start_server()
