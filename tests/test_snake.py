"""Testes automatizados do jogo Snake (executar na raiz: python -m unittest discover tests)."""
import os
import unittest

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

from src.games import snake
from src.game_tools import sprite


class SnakeTests(unittest.TestCase):

    def setUp(self):
        snake.setup()
        snake.new_game()

    def test_setup_carrega_todas_as_imagens(self):
        # Antes: AttributeError ('dict' sem iteritems) no Python 3
        self.assertEqual(set(snake.images), set(snake.image_infos))

    def test_rand_pos_sempre_dentro_da_grade(self):
        # Antes: random.randrange(float) levantava TypeError
        for _ in range(500):
            x, y = snake.rand_pos()
            self.assertTrue(0 < x < snake.WIDTH and 0 < y < snake.HEIGHT)
            self.assertEqual(x % snake.UNIT, 0.5 * snake.UNIT)
            self.assertEqual(y % snake.UNIT, 0.5 * snake.UNIT)

    def test_controle_aceita_teclas_validas_e_ignora_invalidas(self):
        # Antes: dict.has_key não existe no Python 3
        rot = snake.snake.head.rot
        snake.snake.control('left')
        self.assertEqual(snake.snake.head.rot, (rot + 1) % 4)
        snake.snake.control('d')
        self.assertEqual(snake.snake.head.rot, rot)
        snake.snake.control('x')
        self.assertEqual(snake.snake.head.rot, rot)

    def test_comer_comida_aumenta_pontuacao(self):
        snake.food = sprite.Sprite('food', snake.snake.head.pos, [0, 0])
        self.assertTrue(snake.snake.eat_food())
        self.assertEqual(snake.score, snake.POINTS_PER_FOOD)
        self.assertIsNone(snake.food)

    def test_novo_jogo_zera_placar_e_estado(self):
        snake.score = 50
        snake.game_over = True
        snake.new_game()
        self.assertEqual(snake.score, 0)
        self.assertFalse(snake.game_over)

    def test_colisao_com_o_proprio_corpo(self):
        s = snake.snake
        self.assertFalse(s.check_collision())
        s.body.append(sprite.Sprite('seg', s.head.pos, [0, 0]))
        self.assertTrue(s.check_collision())

    def test_nova_comida_nunca_nasce_sobre_a_cobra(self):
        for _ in range(100):
            f = snake.new_food()
            self.assertFalse(snake.snake.is_on(f))

    def test_cobra_atravessa_borda_toroidal(self):
        s = snake.snake
        s.head.pos = (snake.WIDTH - 0.5 * snake.UNIT, s.head.pos[1])
        s.head.vel = (snake.UNIT, 0)
        s.head.update((snake.WIDTH, snake.HEIGHT))
        self.assertEqual(s.head.pos[0], 0.5 * snake.UNIT)


if __name__ == '__main__':
    unittest.main()
