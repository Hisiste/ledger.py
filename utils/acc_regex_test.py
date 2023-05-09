import acc_regex
import unittest


class test_create_ors(unittest.TestCase):
    def test_create_ors(self):
        self.assertEqual(acc_regex.create_ors('Rent Transportation'), 'Rent or Transportation')
        self.assertEqual(acc_regex.create_ors('Income and Job'), 'Income and Job')
        self.assertEqual(acc_regex.create_ors('Radio and (Judge Police)'), 'Radio and (Judge or Police)')

        self.assertEqual(acc_regex.create_ors('(Telephone not Beach) not House'), '(Telephone or not Beach) or not House')

        self.assertEqual(acc_regex.create_ors('Run'), 'Run')


if __name__ == '__main__':
    unittest.main()
