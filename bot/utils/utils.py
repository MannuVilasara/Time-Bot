import pymongo
import dns.resolver

from bot.utils.constants import MONGODB_URI


def mongo():
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
    data = pymongo.MongoClient(MONGODB_URI)
    user = data["Misfit"]["users"]
    return user
