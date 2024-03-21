from itertools import product
from collections import defaultdict
# optimization 1 (worst case)

captchas = ['b5nmm', '53wb8', 'ecd4w', 'y7x8p', 'f6ne5', 'dd5w5', '75pfw', '8y63f', 'gw53m', 'bgd4m', 'ec6pm', 'wce5n', 'xgcxy', 'ndyfe', '4cn7b', 'p4pde', 'x38fn', '3bfnd', 'bbymy', '3w2bw', 'pmf5w', '6dd2y', 'x4gg5', '7gmf3', 'ggd7m', 'cnwyc', '6e6pn', 'xbcbx', '2g783', '3den6', 'dn26n', 'pm363', 'f75cx', 'x3fwf', 'b28g8', 'd378n', '5n245', '8n5pn', 'pdyc8', 'x4f7g', 'xe8xm', 'myc3c', '3bd8f', 'nf8b8', 'pcede', '28x47', 'bdg84', 'mgw3n', '2cg58', 'b6f2p', '47e4p', '264m5', 'fc6xb', 'n3ffn', '7xd5m', '8gecm', 'bw6n6', '8w754', 'yd755', '387g2', 'n2by7', '6gnm3', 'n373n', 'pf5ng', 'xngxc', 'nnn5p', 'en4n4', 'cfc56', '4dgf7', 'nnfx3', '2b827', '3ebnn', 'c2pg6', '6xxdx', 'be3bp', '2ycn8', 'nbcgb', 'gnc3n', '88y52', 'cpc8c', 'cen55', 'nc4yg', 'y5dpp', 'dn5df', 'de45x', '52447', '573d8', 'd6fcn', 'wc2bd', 'cgcgb', '74eyg', 'w52fn', '44xe8', '3nw7w', '73mnx', 'm3588', '34pcn', 'y5w28', 'dpbyd', '7y2x4', '8pfxx', 'y7mnm', 'ny8np', '6p7gx', 'bw44w', '2x7bm', '58b5m', 'd22bd', '7wnpm', 'p2m6n', 'bnc2f', 'wg625', '66wp5', 'g78gn', 'nbfx5', 'nnn57', '8c23f', '3pe4g', 'c86md', 'b84xc', 'e7x45', 'ebcbx', 'w8f36', '33p4e', 'mp7wp', 'cffp4', 'gfp54', 'nbf8m', '64m82', 'bny4w', 'y4n6m', 'gc277', 'c2fb7', 'mm3nn', '77n6g', '3p4nn', '25egp', '7wyp4', 'dbex3', '5ng6e', 'gny6b', '3ny45', 'm67b3', 'x6b5m', 'ng2gw', 'nbp3e', 'dbfen', 'yf424', 'cdcb3']

countries = ['Slovenia', 'China', 'Finland', 'Philippines', 'Nigeria', 'Bulgaria', 'Chile', 'Estonia', 'Liberia', 'New Zealand', 'Portugal', 'Singapore', 'Brazil', 'Croatia', 'Latvia', 'Albania', 'Poland', 'Indonesia', 'Sweden', 'Nepal', 'Romania', 'Netherlands', 'Canada', 'Botswana', 'Iceland', 'Lithuania', 'Austria', 'Australia', 'El Salvador', 'Ghana', 'Japan', 'Georgia', 'Belgium', 'Belarus', 'Norway', 'Israel', 'Peru', 'Venezuela', 'Russia', 'Malaysia', 'Cambodia', 'Jordan', 'Spain', 'Italy', 'Kuwait', 'Madagascar', 'Qatar', 'India', 'Kenya', 'Iran', 'Hungary', 'Colombia', 'Denmark', 'Germany']

chess_sols = ['Rxf5+', 'Nf5+', 'Ne7+', 'Qc8+', 'Ne4+', 'Qxh3+', 'Rxf7+', 'Nf6+', 'Qg2+', 'Qd8+', 'Nh8+', 'Bxf3+', 'Qe7+', 'Bh5+', 'Bf4+', 'Qxf2+', 'Ng3+', 'Qxh6+', 'Nd3+', 'Rxf6+', 'Qf8+', 'Rxa7+', 'Qh8+', 'Qxc6+', 'Bh6+', 'Bf7+', 'Rh8+', 'Qg1+', 'Rg7', 'Rf7+', 'Rxe8+', 'Qd5+', 'Qxd7+', 'Bf6+', 'Qxg6+', 'Nb5+', 'Qf7+', 'Rf8+', 'Ne2+', 'Qxg7+', 'Bf5+', 'g4+', 'Rxh6+', 'Ra1+', 'Qxh7+', 'Bh6', 'Nxd7+', 'Qh3+', 'Qxh5+', 'Nxb7+', 'Rf6', 'Re5+', 'Nd5+', 'Rh6', 'Rh4+', 'Be1+', 'Rxb6+', 'g5+', 'Qxe6+', 'Qb8+', 'Ng6+', 'Qb5+', 'Qc6+', 'Qg7+', 'Qd7+', 'Qh6+', 'Bb5+', 'Qe6+', 'Rxh7+', 'Qxh2+', 'Rxf1+', 'Ng4', 
              'Qh7+', 'Re7+', 'Bf2+', 'Qh5+', 'Rxf8+', 'Qf6+', 'Qe8+', 'Rxh2+', 'Ne6+', 'Qxe8+', 'Qxf7+', 'Bxg6+', 'Rf1+', 'Rf6+', 'Qg4+', 'Qxb8+', 'f2+', 'f5+', 'Rg2+', 'Rg1+', 'Re8+', 'Rxg7+', 'Rg8+', 'Qf5+', 'Rxd8+', 'Nh4+', 'Qxa3+', 'Be5+', 'Be3+', 'Bb6+', 'Ne7', 'Nf4+', 'Rxg6+', 'Nxf7+', 'Nf7+', 'Bd6+', 'Qh2+', 'Rh6+', 'Nf3', 'Ne5+', 'Qg6+', 'Qg8+', 'Qc6', 'Qxc3+', 'Bg6+', 'h5+', 'Re4+', 'Qxd6+', 'Qxf8+', 'Nd4+', 'Rd8+', 'Rc1+', 'Rxe6+', 'Rc8+', 'Qh1+', 'Rh2+', 'Rxh3+', 'Kh6', 'Qxb7+', 'Qc3+']

sponsors = ['pepsi', 'starbucks', 'shell']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
affirmations = ['i am loved', 'i am worthy', 'i am enough']

roman = ['XXXV', 'VII']

youtube = ['youtu.be/']

primes = ['29', '31', '37', '41', '43', '47', '53']

lists = [captchas, countries, chess_sols, sponsors, months, affirmations, roman, youtube, primes]

# for chess_move in chess_sols:

def find_optimal_captchas():
    best_captchas = []
    for captcha in captchas:
        count = 0
        for letter in captcha:
            if letter >= 'a' and letter <= 'f':
                count += 1
        if count >= 4:
            best_captchas.append(captcha)
    return best_captchas

def find_best_moves():
    best_moves = []
    for move in chess_sols:
        if len(move) <= 3 and not move.endswith('+'):
            best_moves.append(move)
    return best_moves

def find_overlap_length(str1, str2):
    overlap = 0
    for i in range(min(len(str1), len(str2)), 0, -1):
        if str1[-i:] == str2[:i]:
            overlap = i
            break
    return overlap

def lowercase_strings():
    for index, lst in enumerate(lists):
        for i in range(len(lst)):
            lists[index][i] = lists[index][i].lower()

def find_all_overlap(lists=lists):
    all_overlap = defaultdict(list)
    for index, lst1 in enumerate(lists):
        for lst2 in lists[:index] + lists[index+1:]:
            for str1 in lst1:
                for str2 in lst2:
                    overlap = find_overlap_length(str1, str2)
                    if overlap > 0:
                        all_overlap[overlap].append((str1, str2))
                    if str1 in str2:
                        all_overlap[len(str1)].append((str1, str2))
    return all_overlap

lowercase_strings()
all_overlap = find_all_overlap([['pcede', 'ebcbx', 'dbfen', 'cdcb3'], ['may', 'june', 'july'], ['pepsi', 'shell'], ['peru', 'iran', 'china', 'chile', 'nepal', 'ghana', 'japan', 'spain', 'italy', 'qatar', 'india', 'kenya'], ['rh6', 'ng4', 'ne7', 'nf3', 'qc6', 'kh6'],
                               ['i am loved', 'i am worthy', 'i am enough'], ['XXXV', 'VII', 'V'], ['youtu.be/']])
print(all_overlap)