from django.test import TestCase
from django.contrib.auth.models import User
from Game.models import Wallet, Asset, Ownership
from Game import interface_control as ic


class InterfaceControlTest(TestCase):

    def setUp(self):
        ic.API_URL = 'http://localhost:8000/tests/'
        user = User.objects.create(username='test_user')
        Wallet.objects.create(user=user)

    def test_ic_sanity(self):
        # search for the names
        assets_name = ic.get_asset_names()
        self.assertNotEqual(assets_name, [])

        # search for all info
        asset_info = [ic.get_asset_quote(a) for a in assets_name if ic.has_quote(ic.get_asset_quote(a))]
        self.assertNotEqual(asset_info, [])

        # dedicated full method
        assets_complete = ic.get_assets()
        self.assertNotEqual(assets_complete, [])

    def test_ic_border(self):
        # ask for a quote of unexistent asset
        asset = ic.AssetStruct(name="NONE", asset_type="NONE")
        quote = ic.get_asset_quote(asset)
        self.assertEqual(quote.buy, -1)
        self.assertEqual(quote.sell, -1)

        # ask for a quote of existent asset
        asset = ic.AssetStruct(name="MARSHALL", asset_type="currency")
        quote = ic.get_asset_quote(asset)
        self.assertNotEqual(quote.buy, -1)
        self.assertNotEqual(quote.sell, -1)

    def test_wallet_sanity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = ic.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name, type=asset_a.type)
        asset_b = assets[1]
        asset_b = Asset.objects.create(name=asset_b.name, type=asset_b.type)
        asset_c = assets[3]
        asset_c = Asset.objects.create(name=asset_c.name, type=asset_c.type)

        # create and save transactions
        Ownership.objects.create(asset=asset_a, quantity=3, wallet=wallet)
        Ownership.objects.create(asset=asset_b, quantity=1, wallet=wallet)
        Ownership.objects.create(asset=asset_c, quantity=5, wallet=wallet)

        # check algorithm response
        response = Wallet.get_info(user)
        self.assertFalse(response['error'])
        expected_assets = [ic.get_asset_quote(asset_a.as_struct()), ic.get_asset_quote(asset_c.as_struct())]
        result_assets = response['assets']
        self.assertEqual(len(result_assets), len(expected_assets))

        for e, r in zip(expected_assets, result_assets):
            self.assertEqual(e.name, r.name)
