from tests.utils import MusicShareTestBase, fake


class TestLoginView(MusicShareTestBase):
    def setUp(self):
        self.password = "F4nf0r]4ll"
        self.user = self.create_login(password=self.password)

    def test_login(self):
        query = """mutation { tokenAuth(email: "%(email)s", 
                                        password: "%(password)s") {
                            token
                            payload
                            success
                    } 
                }
        """ % {'email': self.user.email, 'password': self.password}
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        self.assertTrue(executed.data['tokenAuth']['success'])
        
        self.assertTrue(bool(executed.data['tokenAuth']['token']))
        self.assertEqual(executed.data['tokenAuth']['payload']['email'], 
                         self.user.email)
        self.assertAlmostEqual(
            (executed.data['tokenAuth']['payload']['exp']-executed.data['tokenAuth']['payload']['origIat'])//60,
            20
        )

        #TODO: test rest of errors.
