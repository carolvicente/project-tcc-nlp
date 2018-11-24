from twython import exceptions

'''

Standard Search API

180 req/15 min

8 Personas

22 Requests per persona


* Função para bater API_REQUEST_QTY vezes sendo X vezes por Personas
    - Se CURRENT_REQUEST_QTY == 0
        - Bate em api para ver se o CURRENT_INTERVAL == 0
            Senão:
                - Continua consultando API de Tempo
            Se sim:
                - Volta a coletar dados


'''


def request_time_missing_to_reset(twitter):

    try:
        epoch_time = twitter.get_lastfunction_header(
            'x-rate-limit-reset')

        a = int(epoch_time)
        b = int(time.time())  # current epoch time
        c = a - b  # returns seconds
        minutes = c // 60 % 60
        return minutes
    except Exception as ex:
        template = "Ready to Call Again!"
        return '1'
    except exceptions.TwythonRateLimitError as ex:
        print('Too many requests! Error 429')
        return '429'


def request_quantity_remaining(twitter):

    try:
        qtd = twitter.get_lastfunction_header(
            'x-rate-limit-remaining')
        return int(qtd)
    except Exception as ex:
        template = "Ready to Call Again!"
        print(template)
        return 1
    except exceptions.TwythonRateLimitError as ex:
        print('Too many requests! Error 429')
        return '429'
