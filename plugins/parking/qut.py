from disco.types.message import MessageEmbed
import requests
import json

def get_parking_qut():
    """Replies with an embed object containing QUT parking information"""
    url = "https://paseweb.parkassist.com/sites/qut/status/v2/zones.json"  # URL that has the parking info
    embed = MessageEmbed()  # Create a discord embed object

    # Specify the name, logo, url and description of the parking bot response
    embed.set_author(name='QUT Parking Bot',
                     icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/QUTLogo.svg/1200px-' +
                              'QUTLogo.svg.png')
    embed.url = 'https://paseweb.parkassist.com/en/sites/qut/embedded_widgets/available_spaces'
    embed.description = 'This is scraped from the parkassist website. Only Gardens Point is supported at the moment.'

    response = requests.get(url)  # Fetch the parking info

    if response.status_code == 200:  # If we got an ok response parse the JSON
        parking = json.loads(response.text)
        p = 0
        freeway = 0
        szc = 0

        # This bit of hackery is needed because the parking json segments each level into a separate zone
        for zone in parking["response"]:
            if zone["id"] in [1, 2]:
                p += zone["counts"]["available"]
            elif zone["id"] in [3]:
                freeway += zone["counts"]["available"]
            elif zone["id"] in [4, 5, 6, 7, 8, 9]:
                szc += zone["counts"]["available"]

        # Add each zone to the parking bot response
        embed.add_field(name='P Block (GP)', value='{} parks available.'.format(p), inline=True)
        embed.add_field(name='Under Freeway (GP)', value='{} parks available.'.format(freeway), inline=True)
        embed.add_field(name='S/Z/C Block (GP)', value='{} parks available.'.format(szc), inline=True)
        embed.add_field(name="Last update from QUT:", value=parking["response"][0]["counts"]["timestamp"][11:19],
                        inline=False)

    else:  # If we didn't get an OK response then something went wrong
        embed.add_field(name='Data Not Available', value='Something went wrong while fetching the parking data. This '
                                                         'is most likely a problem with the server the data '
                                                         'comes from.', inline=False)

    # Add some more info to the end of the parking bot response
    embed.add_field(name='More Info', value='For more info about costs and restrictions see this web page: ' +
                                            "https://www.qut.edu.au/about/services-and-facilities/all-services/parking",
                    inline=False)

    return embed  # return the embed object so the parent function can send a response
