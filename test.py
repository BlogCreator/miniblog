def generator():
    request = yield
    print('pre process')
    response = yield
    print('behand process')

if __name__ == '__main__':
    gen = generator()
    next(gen)
    gen.send('request')
    gen.send('response')
