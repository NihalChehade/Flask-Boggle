from unittest import TestCase
from app import app
from flask import session,request
from boggle import Boggle

app.config['TESTING'] = True
class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_board_home(self):
        """Stuff to do before every test."""
        with app.test_client() as client:

            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('<table class="grid-container">', html)
            self.assertIn('You have', html)
            self.assertIn('<div id="score-div">', html)

    def test_checking_suggestion(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] =  [["S", "A", "D", "O", "H"], 
                                     ["S", "A", "D", "O", "H"], 
                                     ["S", "A", "D", "O", "H"], 
                                     ["S", "A", "D", "O", "H"], 
                                     ["S", "A", "D", "O", "H"]]
            res = client.get('/check-guessed?word=sad')
            json = res.json['result']
            self.assertEqual(res.status_code, 200)
            self.assertEqual('ok', json)

            res1 = client.get('/check-guessed?word=bad')
            json1 = res1.json['result']
            self.assertEqual('not-on-board', json1)

            res2 = client.get('/check-guessed?word=dffgdfgfd')
            json2 = res2.json['result']
            self.assertEqual('not-word', json2)


    def test_end_Game(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore'] = 8
                
            res = client.post('/ending-game', data = {'score': 10})
            # import pdb
            # pdb.set_trace()

              
            # score = request.json['score']
            self.assertEqual(res.status_code, 200)
            self.assertIn('highscore', session)
            self.assertEqual(session['num_played'], 1)
            self.assertEqual(session['highscore'], 8)

            
            