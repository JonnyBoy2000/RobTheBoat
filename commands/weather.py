import os
import forecastio
import mapq
import requests as req

from discord.ext import commands
from utils.sharding import darkskyapi, mapquestapi

api_key = darkskyapi
mapquestapistuff = mapquestapi

def mapquest(api_key=mapquestapistuff):
    """Save or request your Mapquest API key."""
    if api_key:
        os.environ['MAPQUEST_API_KEY'] = api_key
    else:
        api_key = os.getenv('MAPQUEST_API_KEY', '')
    return api_key

def location(place):
    """Find the latitude and longitude for a location."""
    map_key = mapquest()
    if map_key == '':
        raise Exception('No MAPQUEST_API_KEY found.')
    results = mapq.latlng(place)
    return (results['lat'], results['lng'])


def _check_lat_lng(lat, lng):
    """Check whether the latitude and longitude of a coordinate were given."""
    if not lng:
        # Then `lat` is actually a string.
        lat, lng = location(lat)
    return (str(lat), str(lng))

class Weather():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def weather(address: str):
        if len(location) > 5:
            try:
                map_key = mapquest()
                results = mapq.latlng(address)
                await bot.say(forecastio.load_forecast(api_key, results['lat'], results['lng']))
            except Exception as e:
                await bot.say("```py\n{}\n```".format(e))
        else:
            await bot.say("Location isn't found or the given zip code or address is too short. Try again.")

def setup(bot):
    bot.add_cog(Weather(bot))