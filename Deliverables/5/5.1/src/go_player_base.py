import sys, random
sys.path.append('../../../3/3.1/src/')
sys.path.append('../../../4/4.1/src/')
from stone import StoneEnum
from point import Point
from output_formatter import format_board
from constants import PASS
from move_referee import MoveReferee
from constants import GAME_OVER, GAME_OVER_RESPONSE



class GoPlayerBase:

   ## Decorators
   def valid_stone(func):
      def wrapper(*args, **kwargs):
         if not args[1] or not isinstance(args[1], StoneEnum):
            raise Exception("GPB: Invalid parameter, bad stone passed.")
         return func(*args, **kwargs)
      return wrapper


   def protocol_registered(func):
      def wrapper(*args, **kwargs):
         if not args[0].name:
            raise Exception("GPB: Invalid protocol, player must be registered first.")
         return func(*args, **kwargs)
      return wrapper


   def protocol_stone_set(func):
      def wrapper(*args, **kwargs):
         if not args[0].stone_type:
            raise Exception("GPB: Invalid protocol, stone must be received first.")
         return func(*args, **kwargs)
      return wrapper



   ## Constructor
   def __init__(self, name=None):
      """
      This class implements a Go Player who chooses
      moves using a dumb strategy of the first valid
      minimum column, minimum row position on the board.
      """
      self.name = name
      self.default_name = "default_player" #"no name"
      self.stone_type = None
      self.move_referee = MoveReferee()


   ## Public Methods
   def register(self):
      if not self.name:
         self.name = self.default_name
      return self.name


   @valid_stone
   @protocol_registered
   def receive_stone(self, stone_type):
      self.stone_type = stone_type


   @protocol_registered
   @protocol_stone_set
   def choose_move(self, boards):
      """
      if not self.move_referee.valid_history(self.stone_type, boards):
            return "This history makes no sense!"
      for x, y in sorted(list(boards[0].get_points(None))):
         if self.move_referee.valid_move(self.stone_type, Point(x, y), boards, boards[0]):
            return (x, y)
      else:   
         return PASS
      """

      epsilon = 0.3
      roll = random.random()

      if roll > epsilon:
         if not self.move_referee.valid_history(self.stone_type, boards):
            return "This history makes no sense!"
         for x, y in sorted(list(boards[0].get_points(None))):
            if self.move_referee.valid_move(self.stone_type, Point(x, y), boards, boards[0]):
               return (x, y)
         else:   
            return PASS
      
      else:   
         return PASS


   def game_over(self, end_tag):
      # Reset default player for next game
      if end_tag == [GAME_OVER]:
         self.stone_type = None
         self.move_referee = MoveReferee()
         return True
      else:
         return False