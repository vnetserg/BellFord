# -*- coding: utf-8 -*-

class Model:
    def __init__(self):
        self._currencies = []
        self._ratios = {}

    def addCurrency(self, cur):
        if cur in self._currencies:
            raise ValueError("Currency already in model!")
        for oth in self._currencies:
            self._ratios[tuple(sorted((oth, cur)))] = 1.0
        self._currencies.append(cur)

    def deleteCurrency(self, cur):
        if cur not in self._currencies:
            raise ValueError("No such currency in model!")
        self._currencies.remove(cur)
        for oth in self._currencies:
            del self._ratios[tuple(sorted((oth, cur)))]

    def deleteCurrencyNum(self, num):
        if not (0 <= num < len(self._currencies)):
            raise ValueError("Invalid currency number!")
        cur = self._currencies[num]
        del self._currencies[num]
        for oth in self._currencies:
            del self._ratios[tuple(sorted((oth, cur)))]

    def renameCurrency(self, old, new):
        if old not in self._currencies:
            raise ValueError("No such currency in model!")
        self._currencies[self._currencies.index(old)] = new
        for cur in self._currencies:
            if cur != new:
                self._ratios[tuple(sorted((cur, new)))] = self._ratios[tuple(sorted((cur, old)))]
                del self._ratios[tuple(sorted((cur, old)))]

    def hasCurrency(self, cur):
        return cur in self._currencies

    def getCurrency(self, num):
        if not (0 <= num < len(self._currencies)):
            raise ValueError("Invalid currency number!")
        return self._currencies[num]

    def numCurrencies(self):
        return len(self._currencies)

    def currencyIndex(self, cur):
        try:
            return self._currencies.index(cur)
        except ValueError:
            raise ValueError("No such currency in model!")

    def currencies(self):
        return tuple(self._currencies)

    def getRatio(self, cur1, cur2):
        for cur in (cur1, cur2):
            if cur not in self._currencies:
                raise ValueError("No such currency in model!")
        if cur1 == cur2:
            return 1.0
        key = tuple(sorted((cur1, cur2)))
        if key[0] == cur1:
            return self._ratios[key]
        else:
            return 1.0/self._ratios[key]

    def setRatio(self, cur1, cur2, ratio):
        for cur in (cur1, cur2):
            if cur not in self._currencies:
                raise ValueError("No such currency in model!")
        if ratio <= 0:
            raise ValueError("Invalid ratio!")
        key = tuple(sorted((cur1, cur2)))
        if key[0] == cur1:
            self._ratios[key] = ratio
        else:
            self._ratios[key] = 1.0/ratio