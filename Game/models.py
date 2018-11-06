from django.db import models
from django.contrib.auth.models import User
from Game.interface_control import AssetComunication as ACommunication
import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


# /*
# TODO: separar todos los modelos en archivos distintos
# */


class Asset(models.Model):
    name = models.CharField(max_length=75, primary_key=True, unique=True)
    type = models.CharField(max_length=10)
    # non persistent data
    buy = -1
    sell = -1
    quantity = -1

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "buy": self.buy,
            "sell": self.sell,
            "quantity": self.quantity
        }

    def is_valid(self):
        return self.sell != -1 and self.buy != -1

    @staticmethod
    def create_if_not_exists(name):
        asset = Asset.safe_get(name)
        if not asset:
            asset_comms = ACommunication(settings.API_URL)
            type = asset_comms.get_asset_type(name)
            if not type:
                return None
            asset = Asset.objects.create(name=name, type=type)
            asset.save()
        return asset

    @staticmethod
    def safe_get(name):
        try:
            return Asset.objects.get(name=name)
        except ObjectDoesNotExist:
            return None


class Wallet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liquid = models.FloatField(null=False, default=10000)
    assets = models.ManyToManyField(Asset, through='Ownership')
    image = models.ImageField(upload_to='profile_image',
                              default='profile_image/no_image.jpg')

    @staticmethod
    def get_info(user):
        """
        full wallet info given user
        :param user:
        :return dict {assets: [Asset], value_wallet: Float, error: Bool}
        """
        response = {}
        wallet = Wallet.objects.get(user=user)
        response['liquid'] = wallet.liquid
        value_wallet = wallet.liquid
        ownerships = Ownership.objects.filter(wallet=wallet, quantity__gt=0)
        assets = []
        asset_communication = ACommunication(settings.API_URL)
        for o in ownerships:
            asset = asset_communication.get_asset_quote(o.asset)
            asset.quantity = o.quantity
            value_wallet += o.quantity * asset.sell
            assets.append(asset)
        response['assets'] = assets
        response['value_wallet'] = value_wallet
        response['error'] = False
        return response

    def buy_asset(self, asset):
        """
        add an asset to the user wallet and add the transaction to user history
        :param asset:
        :return: dict {error: Bool, message: String}
        """
        asset_comms = ACommunication(settings.API_URL)
        asset = asset_comms.get_asset_quote(asset)
        price = (asset.buy * asset.quantity)
        buy = asset.buy
        sell = asset.sell
        quantity = asset.quantity
        name = asset.name
        type = asset.type

        if quantity <= 0:
            return {"error": True,
                    "message": "You need to buy at least one asset"}

        if self.liquid >= price:
            asset = Asset.safe_get(name=asset.name)
            # if not asset then create one
            if not asset:
                asset = Asset(name=name,
                              type=type)
                asset.save()

            asset.quantity = quantity
            asset.buy = buy
            asset.sell = sell
            ownership = Ownership.safe_get(wallet=self, asset=asset)
            # if not ownership then create one
            if not ownership:
                ownership = Ownership(asset=asset, wallet=self,
                                      quantity=asset.quantity)
            else:
                ownership.quantity += quantity
                ownership.quantity = round(ownership.quantity, 3)
            ownership.save()

            Transaction(wallet=self, asset=asset, asset_price_buy=asset.buy,
                        asset_price_sell=asset.sell,
                        date=datetime.datetime.now(), quantity=quantity,
                        is_purchase=True).save()

            self.liquid -= price
            self.liquid = round(self.liquid, 3)
            self.save()
            return {"error": False, "message": "Purchase has been successful"}
        else:
            return {"error": True, "message": "Not enough cash"}

    def sell_asset(self, asset):
        """
        remove an asset to the user wallet and
        add the transaction to user history.
        :param asset:
        :return: dict {error: Bool, message: String}
        """
        asset_comms = ACommunication(settings.API_URL)
        asset = asset_comms.get_asset_quote(asset)
        price = (asset.sell * asset.quantity)
        quantity = asset.quantity

        if quantity <= 0:
            return {"error": True,
                    "message": "You need to sell at least one asset"}

        ownership = Ownership.safe_get(wallet=self, asset=asset)
        if not ownership:
            return {"error": True, "message": "You do not own this asset"}

        if asset.quantity > ownership.quantity:
            return {"error": True, "message": "Not enough assets"}

        if asset.quantity == ownership.quantity:
            ownership.delete()
        else:
            ownership.quantity -= asset.quantity
            ownership.quantity = round(ownership.quantity, 3)
            ownership.save()

        Transaction(wallet=self, asset=asset, asset_price_buy=asset.buy,
                    asset_price_sell=asset.sell,
                    date=datetime.datetime.now(), quantity=asset.quantity,
                    is_purchase=False).save()

        self.liquid += price
        ownership.quantity = round(self.liquid, 3)
        self.save()
        return {"error": False, "message": "Sale has been succesfull"}


class Ownership(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    @staticmethod
    def safe_get(wallet, asset):
        """
        get a specific ownership, return None if it doesn't exists
        :param wallet, asset:
        :return Ownership
        """
        try:
            return Ownership.objects.get(wallet=wallet, asset=asset)
        except ObjectDoesNotExist:
            return None


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    asset_price_buy = models.FloatField(null=False, default=-1)
    asset_price_sell = models.FloatField(null=False, default=-1)
    date = models.DateField(default=datetime.date.today)
    quantity = models.FloatField()
    is_purchase = models.BooleanField(null=False)

    @staticmethod
    def get_info(wallet):
        """
        search for all made transactions
        :param wallet:
        :return dict {transactions: [Transactions]}:
        """
        response = {}
        transactions = Transaction.objects.filter(wallet=wallet,
                                                  quantity__gt=0)
        response['transactions'] = transactions
        return response


class Alarm(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    price = models.TextField(null=False, default='up')
    threshold = models.FloatField(null=False, default=-1)
    type = models.TextField(null=False, default='up')
    triggered = models.BooleanField(null=False, default=False)
    old_price = models.FloatField(null=False, default=-1)

    def trigger(self):
        acom = ACommunication(settings.API_URL)
        asset = acom.get_asset_quote(self.asset)

        if not asset.is_valid():
            return False

        if self.type == 'up':
            return asset.__getattribute__(self.price) > self.threshold
        else:
            return asset.__getattribute__(self.price) < self.threshold

    def reactivate(self):
        acom = ACommunication(settings.API_URL)
        asset = acom.get_asset_quote(self.asset)
        if self.type == 'up':
            self.triggered = asset.__getattribute__(
                self.price) >= self.threshold
        else:
            self.triggered = asset.__getattribute__(
                self.price) <= self.threshold
        self.save()

    @staticmethod
    def safe_get(wallet, asset, price, type):
        try:
            return Alarm.objects.get(wallet=wallet, asset=asset, price=price,
                                     type=type)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def safe_save(wallet, aname, threshold, atype, price):
        acom = ACommunication(settings.API_URL)
        asset = Asset.create_if_not_exists(aname)
        if not asset:
            return {'error': True, 'message': 'Non existing asset'}

        asset = acom.get_asset_quote(asset)

        if Alarm.safe_get(wallet, asset, price, atype):
            return {'error': True,
                    'message': 'You already have an alarm on this asset'}

        Alarm.objects.create(wallet=wallet, asset=asset,
                             price=price,
                             old_price=asset.__getattribute__(price),
                             threshold=threshold, type=atype).save()
        return {'error': False,
                'message': 'Your alarm has been set successfully!'}

    @staticmethod
    def get_info(wallet):
        alarms = Alarm.objects.filter(wallet=wallet)
        if not alarms:
            return {'error': True, 'message': "You don't have any alarm set"}
        else:
            return {'error': False, 'alarms': alarms}

    @staticmethod
    def safe_delete(wallet, name, atype, price):
        asset = Asset.objects.get(name=name)
        alarm = Alarm.objects.get(asset=asset, wallet=wallet,
                                  type=atype, price=price)
        alarm.delete()
