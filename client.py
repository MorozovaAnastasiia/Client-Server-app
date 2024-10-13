import socket

HOST = '127.0.0.1'
PORT = 65432
history = list()

def show_history():
  print(history)
def run_experiment(s):
  history = {}
  while (True):
    data = input("Введите команду (guess, history): ")
    if data == 'guess':
      guess = 'guess '
      num = int(input("Введите ваше предположение: "))
      guess += str(num)
      s.sendall(str(guess).encode('utf-8'))
      response = s.recv(1024).decode('utf-8')
      history.append(num)
      print(f"Сервер ответил: {response}")
      if (response == 'You guessed it!'):
        break
    elif data == 'history':
      show_history()
      pass
    else:
      print("Неверная команда.")

def start_client():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Подключение к серверу...")

    while True:
      print("Ожидаем начала эксперимента")
      data = s.recv(1024).decode('utf-8')
      print(f"Сервер ответил: {data}")
      if data == 'Experiment started!':
        run_experiment(s)
      elif data == 'Эксперимент уже начался.':
        print('Выходим, так как эксперимент уже идет')
        break
    

if __name__ == '__main__':
  start_client()
