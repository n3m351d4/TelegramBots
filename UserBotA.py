import copy
from random import Random
from datetime import datetime
from random import randrange
from datetime import timedelta
from random import randint
from mimesis import Address, locales
from mimesis import Person



async def privateparser(client, event):
    chat = await client.get_entity(event.chat_id)
    user = await client.get_entity(event.message.from_id)
    print(chat)
    chatname = chat.title
    chat = await client.get_entity(-1) # куда форвардим
    await client.send_message(chat, 'Зафиксировали в ' + chatname)
    await event.forward_to(-1) # куда форвардим

async def cvv(client, event):
    visaPrefixList = [['4', '5', '3', '9'], ['4', '5', '5', '6'], ['4', '9', '1', '6'], ['4', '5', '3', '2'], ['4', '9', '2', '9'], ['4', '0', '2', '4', '0', '0', '7', '1'], ['4', '4', '8', '6'], ['4', '7', '1', '6'], ['4']]
    mastercardPrefixList = [['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]
    amexPrefixList = [['3', '4'], ['3', '7']]
    discoverPrefixList = [['6', '0', '1', '1']]
    dinersPrefixList = [ ['3', '0', '0'], ['3', '0', '1'], ['3', '0', '2'], ['3', '0', '3'], ['3', '6'], ['3', '8']]
    enRoutePrefixList = [['2', '0', '1', '4'], ['2', '1', '4', '9']]
    jcbPrefixList = [['3', '5']]
    voyagerPrefixList = [['8', '6', '9', '9']]

    def random_date(start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60)
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def completed_number(prefix, length):
        """
        'prefix' is the start of the CC number as a string, any number of digits.
        'length' is the length of the CC number to generate. Typically 13 or 16
        """
        ccnumber = prefix
        # generate digits
        while len(ccnumber) < (length - 1):
            digit = str(generator.choice(range(0, 10)))
            ccnumber.append(digit)
        # Calculate sum
        sum = 0
        pos = 0
        reversedCCnumber = []
        reversedCCnumber.extend(ccnumber)
        reversedCCnumber.reverse()
        while pos < length - 1:
            odd = int(reversedCCnumber[pos]) * 2
            if odd > 9:
                odd -= 9
            sum += odd
            if pos != (length - 2):
                sum += int(reversedCCnumber[pos + 1])
            pos += 2
        # Calculate check digit
        checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
        ccnumber.append(str(checkdigit))
        return ''.join(ccnumber)

    def credit_card_number(rnd, prefixList, length, howMany):
        result = []
        while len(result) < howMany:
            ccnumber = copy.copy(rnd.choice(prefixList))
            result.append(str(completed_number(ccnumber, length)).replace(".",""))
        return result

    def time():
        d1 = datetime.now()
        d2 = datetime.now()+timedelta(weeks=192)
        d = random_date(d1, d2)
        expired_date = d.strftime("%m/%y")
        return expired_date

    def cvcfunc():
        cvc = str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9))
        return cvc
    #
    # def get_name():
    #     return names[randint(0, len(names)-1)]
    #
    # def get_lastname():
    #     return lastnames[randint(0, len(lastnames)-1)]

    def adress():
        en = Address('en')
        person = Person(locales.EN)
        name = person.full_name()
        street = en.address()
        country = en.country()
        region = en.region()
        list1 = [name, country, region, street]
        return ' '.join(list1)


    generator = Random()
    generator.seed()  # Seed from current time
    mastercard = credit_card_number(generator, mastercardPrefixList, 16, 1) #print(output("Mastercard", mastercard))
    visa16 = credit_card_number(generator, visaPrefixList, 16, 1)           #print(output("VISA 16 digit", visa16))
    visa13 = credit_card_number(generator, visaPrefixList, 13, 1)           #print(output("VISA 13 digit", visa13))
    amex = credit_card_number(generator, amexPrefixList, 15, 1)             #print(output("American Express", amex))
    discover = credit_card_number(generator, discoverPrefixList, 16, 1)     #print(output("Discover", discover))
    diners = credit_card_number(generator, dinersPrefixList, 14, 1)         #print(output("Diners Club / Carte Blanche", diners))
    enRoute = credit_card_number(generator, enRoutePrefixList, 15, 1)       #print(output("enRoute", enRoute))
    jcb = credit_card_number(generator, jcbPrefixList, 16, 1)               #print(output("JCB", jcb))
    voyager = credit_card_number(generator, voyagerPrefixList, 15, 1)       #print(output("Voyager", voyager))

    msg = f"Visa {visa16[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"Mastercard {mastercard[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"Visa {visa13[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"American Express {amex[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"Discover {discover[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"Diners Club {diners[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"enRoute {enRoute[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"JCB {jcb[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f"Voyager {voyager[0]} {cvcfunc()} {time()} {adress()}\n \n" \
          f""

    await event.message.reply(msg)

