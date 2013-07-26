#prime test
def test(end):
    candidates = range(1,end+1)
    primes = list()
    for candidate in candidates:
        prime = True
        for prime in primes:
            if candidate % prime:
                test_result = ((prime ** (candidate - 1)) % candidate)
                print "Candidate: %s, Prime: %s, Result:%s" %(candidate,prime,test_result)
                if test_result != 1:
                    prime = False
                    break
        if prime:
            primes.append(candidate)
    return primes

test(100)
