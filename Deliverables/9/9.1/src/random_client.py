import sys, json, socket, time, random
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../5/5.1/src/')
sys.path.append('../../../5/5.2/src/')
from stone import StoneEnum, Stone, make_stone
from point import get_raw
from obj_parser import parse_stone, parse_boards
from output_formatter import format_board
from constants import REGISTER, RECEIVE, MOVE, EMPTY_STONE, WHITE_STONE, BLACK_STONE, GAME_OVER, GAME_OVER_RESPONSE, BOARD_DIM
from go_player_base import GoPlayerBase
from go_player_adv import GoPlayerAdv


class GoRemotePlayer():

	def __init__(self, n=1, player_type="always_valid"):
		self.player = GoPlayerAdv(n=1, name="player-no{}".format(random.randint(0, 750)))
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.game_over = False
		self.player_type = player_type


	def turn_on_socket(self, ip_and_port):
		self.socket.connect(ip_and_port)


	def work_with_socket(self):
		try:
			inpt = self.socket.recv(8192)
			print("received")
			print(inpt)
			output = self.work_JSON(json.loads(inpt.decode("utf-8")))
			if not output:
				pass
			else:
				print('sending')
				print(output)
				self.socket.sendall(bytes(output, "utf-8"))
				print('sent')
		except:
			self.game_over = True
			print("The game is now over.")
			#print("Error: something went wrong. Either disconnected, or received invalid input.")

	def turn_off_socket(self):
		self.socket.close()


	def work_JSON(self, obj):
		print("working with socket")
		if obj[0] == REGISTER:
			output = self.register()
		
		elif obj[0] == RECEIVE:
			if obj[1] == BLACK_STONE:
				stone_e = StoneEnum.BLACK
			elif obj[1] == WHITE_STONE:
				stone_e = StoneEnum.WHITE
			else:
				print("RC: Invalid stone type.")
				raise Exception()
			self.receive_stone(stone_e)
			output = None
			return output
		
		elif obj[0] == MOVE:
			boards_obj = parse_boards(obj[1])
			print("trying")
			output = self.make_a_move(boards_obj)
			print("found one")
			
			if isinstance(output, tuple):
				output = get_raw(output)
		
		elif obj[0] == GAME_OVER:
			output = GAME_OVER_RESPONSE
		else:
			print("RC: Invalid JSON input.")
			raise Exception()
		output = "\"" + output + "\""
		return output		


	def register(self):
		return self.player.register()


	def receive_stone(self, stone_type):
		if isinstance(stone_type, StoneEnum):
			self.player.receive_stone(stone_type)
		else:
			print("RC: Not a proper player stone.")
			raise Exception()


	def make_a_move(self, board_history):
		#return input("choose_move:")
		if self.player_type == "always_valid":
			espilon = random.uniform(0,1)
			if espilon > .15:
				return self.player.choose_move(board_history)
			else:
				return "pass"
		
		elif self.player_type == "random_point":
			x = random.randrange(1,BOARD_DIM)
			y = random.randrange(1,BOARD_DIM)
			return (x, y)
		
		elif self.player_type == "pass":
			return "pass"
		
		elif self.player_type == "mostly_invalid":
			x = random.randrange(1,BOARD_DIM*2)
			y = random.randrange(1,BOARD_DIM*2)
			return (x, y)

		elif self.player_type == "1-1":
			return (1, 1)
		
		elif self.player_type == "always_invalid":
			return "whoopity scoop $@%$%!@56"

		elif self.player_type == "disconnect":
			self.turn_off_socket()
			return

		else:
			print("Invalid player type.")
			raise Exception()

if __name__ == "__main__":
	print("launched")
	go_config = json.load(open('go.config'))
	HOSTNAME = go_config['IP']
	PORT = go_config['port']

	inputs = sys.argv
	if len(inputs) == 2:
		if inputs[1] in ["always_valid", "random_point", "pass", "mostly_invalid", "1-1", "always_invalid", "disconnect"]:
			player_type = inputs[1]
	else:
		player_type = "always_valid"

	time.sleep(1)
	print("running")
	player = GoRemotePlayer(player_type=player_type)
	player.turn_on_socket((HOSTNAME, PORT))
	while not player.game_over:
		player.work_with_socket()

	"""
	done = 0
	while done != 0.05:
		player.work_with_socket()
		done += 1
	"""

	player.turn_off_socket()