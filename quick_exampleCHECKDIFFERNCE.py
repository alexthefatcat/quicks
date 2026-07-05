# -*- coding: utf-8 -*-
"""Created on Sun Nov 19 16:53:28 2023@author: alexm"""
from io import StringIO
import pandas as pd

def __create_image():
    import numpy as np
    img = np.zeros([400,400,3])
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            #red square
            if 190>i>10:
                if 190>j>10:
                    img[i,j,0] = 1
                    
            #blue circle
            if (i-100)**2 +(j-300)**2 <90**2:
                img[i,j,2] = 1
                continue                 
            
            
            #Add Grid
            #white lines Horizontal
            if i in list(range(50,img.shape[0],50))+list(range(51,img.shape[0],100)):
                img[i,j,:] = 1                 
                continue
            #white lines Vertical            
            if j in range(50,img.shape[1],50):
                img[i,j,:] = 1
                continue                
                
                    
            #green traingle
            n = (3/2)**0.5
            i2, j2 = i-250, j-300        
            if i<350:
                if i2+(n*j2)>0:
                    if i2-(n*j2)>0:
                        img[i,j,1] = 1
                        continue
    
            #small colored boxs
            if 390>i>370 and 360>j>240:
                for ii,cc in enumerate([(1,1,0), (0,1,1), (1,0,1), (1,1,1),(1,0.5,0),(0,1,0.5)]):
                    if (j-240)//20==ii:
                        img[i,j,:]=cc
                        
            #black-white chess board spectrum
            if 219>i>205:        
                if 270>j>205:
                    img[i,j,:] = (i+j)%2==0 if j<240 else (j-240)/30 
                    continue                    
    
    
            # yellow point spread function
            z = 30/(30+(i-250)**2 +(j-245)**2)
            if z>0.01:
                img[i,j,:2] = z      
    
            # spectrum square
            if 110>i>90:        
                if 140>j>60:
                    img[i,j,:] = ((i-90)/(110-90), (j-60)/(140-60),0)                  
            
            #spectrum cross
            if 390>i>210 and 190>j>10:
                if abs((i-300)+(j-100))<10 or abs((i-300)-(j-100))<10:
                    a = max(0,(60-abs(j-10))/60)+max(0,(60-abs(j-190))/40)
                    b = max(0,(60-abs(j-70))/60) 
                    c = max(0,(60-abs(j-130))/60)
                    img[i,j,:] = (a,b,c)
                    
    return img




 

 
def __create_dataframe():
    import pandas as pd
    csv_str = ''',Film,Genre,Lead Studio,Audience score %,Profitability,Rotten Tomatoes %,Worldwide Gross,Year,SEEN_(checkbox)
    0,Zack and Miri Make a Porno,Romance,The Weinstein Company,70,1.747541667,64,$41.94 ,2008,X
    1,Youth in Revolt,Comedy,The Weinstein Company,52,1.09,68,$19.62 ,2010,
    2,You Will Meet a Tall Dark Stranger,Comedy,Independent,35,1.211818182,43,$26.66 ,2010,
    3,When in Rome,Comedy,Disney,44,0.0,15,$43.04 ,2010,X
    4,What Happens in Vegas,Comedy,Fox,72,6.267647029,28,$219.37 ,2008,X
    5,Water For Elephants,Drama,20th Century Fox,72,3.081421053,60,$117.09 ,2011,X
    6,WALL-E,Animation,Disney,89,2.896019067,96,$521.28 ,2008,X
    7,Waitress,Romance,Independent,67,11.0897415,89,$22.18 ,2007,
    8,Waiting For Forever,Romance,Independent,53,0.005,6,$0.03 ,2011,
    9,Valentine's Day,Comedy,Warner Bros.,54,4.184038462,17,$217.57 ,2010,
    10,Tyler Perry's Why Did I get Married,Romance,Independent,47,3.7241924,46,$55.86 ,2007,X
    11,Twilight: Breaking Dawn,Romance,Independent,68,6.383363636,26,$702.17 ,2011,X
    12,Twilight,Romance,Summit,82,10.18002703,49,$376.66 ,2008,X
    13,The Ugly Truth,Comedy,Independent,68,5.402631579,14,$205.30 ,2009,X
    14,The Twilight Saga: New Moon,Drama,Summit,78,14.1964,27,$709.82 ,2009,X
    15,The Time Traveler's Wife,Drama,Paramount,65,2.598205128,38,$101.33 ,2009,X
    16,The Proposal,Comedy,Disney,74,7.8675,43,$314.70 ,2009,X
    17,The Invention of Lying,Comedy,Warner Bros.,47,1.751351351,56,$32.40 ,2009,X
    18,The Heartbreak Kid,Comedy,Paramount,41,2.129444167,30,$127.77 ,2007,X
    19,The Duchess,Drama,Paramount,68,3.207850222,60,$43.31 ,2008,X
    20,The Curious Case of Benjamin Button,Fantasy,Warner Bros.,81,1.78394375,73,$285.43 ,2008,X
    21,The Back-up Plan,Comedy,CBS,47,2.202571429,20,$77.09 ,2010,X
    22,Tangled,Animation,Disney,88,1.365692308,89,$355.01 ,2010,X
    23,Something Borrowed,Romance,Independent,48,1.719514286,15,$60.18 ,2011,
    24,She's Out of My League,Comedy,Paramount,60,2.4405,57,$48.81 ,2010,
    25,Sex and the City Two,Comedy,Warner Bros.,49,2.8835,15,$288.35 ,2010,
    26,Sex and the City 2,Comedy,Warner Bros.,49,2.8835,15,$288.35 ,2010,X
    27,Sex and the City,Comedy,Warner Bros.,81,7.221795791,49,$415.25 ,2008,
    28,Remember Me,Drama,Summit,70,3.49125,28,$55.86 ,2010,
    29,Rachel Getting Married,Drama,Independent,61,1.384166667,85,$16.61 ,2008,X
    30,Penelope,Comedy,Summit,74,1.382799733,52,$20.74 ,2008,X
    31,P.S. I Love You,Romance,Independent,82,5.103116833,21,$153.09 ,2007,
    32,Over Her Dead Body,Comedy,New Line,47,2.071,15,$20.71 ,2008,X
    33,Our Family Wedding,Comedy,Independent,49,0.0,14,$21.37 ,2010,X
    34,One Day,Romance,Independent,54,3.682733333,37,$55.24 ,2011,X
    35,Not Easily Broken,Drama,Independent,66,2.14,34,$10.70 ,2009,X
    36,No Reservations,Comedy,Warner Bros.,64,3.307180357,39,$92.60 ,2007,X
    37,Nick and Norah's Infinite Playlist,Comedy,Sony,67,3.3527293,73,$33.53 ,2008,X
    38,New Year's Eve,Romance,Warner Bros.,48,2.536428571,8,$142.04 ,2011,X
    39,My Week with Marilyn,Drama,The Weinstein Company,84,0.8258,83,$8.26 ,2011,X
    40,Music and Lyrics,Romance,Warner Bros.,70,3.64741055,63,$145.90 ,2007,X
    41,Monte Carlo,Romance,20th Century Fox,50,1.9832,38,$39.66 ,2011,X
    42,Miss Pettigrew Lives for a Day,Comedy,Independent,70,0.2528949,78,$15.17 ,2008,X
    43,Midnight in Paris,Romence,Sony,84,8.744705882,93,$148.66 ,2011,X
    44,Marley and Me,Comedy,Fox,77,3.746781818,63,$206.07 ,2008,X
    45,Mamma Mia!,Comedy,Universal,76,9.234453864,53,$609.47 ,2008,X
    46,Mamma Mia!,Comedy,Universal,76,9.234453864,53,$609.47 ,2008,X
    47,Made of Honor,Comdy,Sony,61,2.64906835,13,$105.96 ,2008,X
    48,Love Happens,Drama,Universal,40,2.004444444,18,$36.08 ,2009,X
    49,Love & Other Drugs,Comedy,Fox,55,1.817666667,48,$54.53 ,2010,X
    50,Life as We Know It,Comedy,Independent,62,2.530526316,28,$96.16 ,2010,X
    51,License to Wed,Comedy,Warner Bros.,55,1.9802064,8,$69.31 ,2007,X
    52,Letters to Juliet,Comedy,Summit,62,2.639333333,40,$79.18 ,2010,X
    53,Leap Year,Comedy,Universal,49,1.715263158,21,$32.59 ,2010,X
    54,Knocked Up,Comedy,Universal,83,6.636401848,91,$219 ,2007,X
    55,Killers,Action,Lionsgate,45,1.245333333,11,$93.40 ,2010,X
    56,Just Wright,Comedy,Fox,58,1.797416667,45,$21.57 ,2010,X
    57,Jane Eyre,Romance,Universal,77,0.0,85,$30.15 ,2011,X
    58,It's Complicated,Comedy,Universal,63,2.642352941,56,$224.60 ,2009,X
    59,I Love You Phillip Morris,Comedy,Independent,57,1.34,71,$20.10 ,2010,X
    60,High School Musical 3: Senior Year,Comedy,Disney,76,22.91313646,65,$252.04 ,2008,X
    61,He's Just Not That Into You,Comedy,Warner Bros.,60,7.1536,42,$178.84 ,2009,X
    62,Good Luck Chuck,Comedy,Lionsgate,61,2.36768512,3,$59.19 ,2007,X
    63,Going the Distance,Comedy,Warner Bros.,56,1.3140625,53,$42.05 ,2010,X
    64,Gnomeo and Juliet,Animation,Disney,52,5.387972222,56,$193.97 ,2011,X
    65,Gnomeo and Juliet,Animation,Disney,52,5.387972222,56,$193.97 ,2011,X
    66,Ghosts of Girlfriends Past,Comedy,Warner Bros.,47,2.0444,27,$102.22 ,2009,X
    67,Four Christmases,Comedy,Warner Bros.,52,2.022925,26,$161.83 ,2008,X
    68,Fireproof,Drama,Independent,51,66.934,40,$33.47 ,2008,X
    69,Enchanted,Comedy,Disney,80,4.005737082,93,$340.49 ,2007,X
    70,Dear John,Drama,Sony,66,4.5988,29,$114.97 ,2010,X
    71,Beginners,Comedy,Independent,80,4.471875,84,$14.31 ,2011,X
    72,Across the Universe,romance,Independent,84,0.652603178,54,$29.37 ,2007,X
    73,A Serious Man,Drama,Universal,64,4.382857143,89,$30.68 ,2009,X
    74,A Dangerous Method,Drama,Independent,89,0.44864475,79,$8.97 ,2011,X
    75,27 Dresses,Comedy,Fox,71,5.3436218,40,$160.31 ,2008,X
    76,(500) Days of Summer,comedy,Fox,81,8.096,87,$60.72 ,2009,X'''

    df = pd.read_csv(StringIO(csv_str),index_col=0)
    df.iloc[:,-1] = df.iloc[:,-1].fillna('')
    return df

text = """It was the best of times, it was the worst of times, it was the age 
of wisdom, it was the age of foolishness, it was the epoch of belief, it was 
the epoch of incredulity, it was the season of Light, it was the season of 
Darkness, it was the spring of hope, it was the winter of despair, we had 
everything before us, we had nothing before us, we were all going direct to 
Heaven, we were all going direct the other way—in short, the period was so far 
like the present period, that some of its noisiest authorities insisted on its 
being received, for good or for evil, in the superlative degree of comparison 
only.""".replace('\\n','')

def func_nth_prime(e):
    #nth_prime
    primes = []
    counter = 1
    while True:
        counter +=1
        for prime in primes:
            if counter%prime==0:
                break
        else:
            primes.append(counter)
        if len(primes)==e:
            return primes[-1]


image = __create_image()
film_df = __create_dataframe()
func = func_nth_prime

# from quick_example import image, film_df, func_nth_prime, text

def __create_dataframe2():
    import pandas as pd
    csv_str = '''Name 	Type 1 	Type 2 	Total 	HP 	Attack 	Defense 	Sp. Atk 	Sp. Def 	Speed 	Generation 	Legendary
    1 	Bulbasaur 	Grass 	Poison 	318 	45 	49 	49 	65 	65 	45 	1 	False
    2 	Ivysaur 	Grass 	Poison 	405 	60 	62 	63 	80 	80 	60 	1 	False
    3 	Venusaur 	Grass 	Poison 	525 	80 	82 	83 	100 	100 	80 	1 	False
    3 	VenusaurMega Venusaur 	Grass 	Poison 	625 	80 	100 	123 	122 	120 	80 	1 	False
    4 	Charmander 	Fire 		309 	39 	52 	43 	60 	50 	65 	1 	False
    5 	Charmeleon 	Fire 		405 	58 	64 	58 	80 	65 	80 	1 	False
    6 	Charizard 	Fire 	Flying 	534 	78 	84 	78 	109 	85 	100 	1 	False
    6 	CharizardMega Charizard X 	Fire 	Dragon 	634 	78 	130 	111 	130 	85 	100 	1 	False
    6 	CharizardMega Charizard Y 	Fire 	Flying 	634 	78 	104 	78 	159 	115 	100 	1 	False
    7 	Squirtle 	Water 		314 	44 	48 	65 	50 	64 	43 	1 	False
    8 	Wartortle 	Water 		405 	59 	63 	80 	65 	80 	58 	1 	False
    9 	Blastoise 	Water 		530 	79 	83 	100 	85 	105 	78 	1 	False
    9 	BlastoiseMega Blastoise 	Water 		630 	79 	103 	120 	135 	115 	78 	1 	False
    10 	Caterpie 	Bug 		195 	45 	30 	35 	20 	20 	45 	1 	False
    11 	Metapod 	Bug 		205 	50 	20 	55 	25 	25 	30 	1 	False
    12 	Butterfree 	Bug 	Flying 	395 	60 	45 	50 	90 	80 	70 	1 	False
    13 	Weedle 	Bug 	Poison 	195 	40 	35 	30 	20 	20 	50 	1 	False
    14 	Kakuna 	Bug 	Poison 	205 	45 	25 	50 	25 	25 	35 	1 	False
    15 	Beedrill 	Bug 	Poison 	395 	65 	90 	40 	45 	80 	75 	1 	False
    15 	BeedrillMega Beedrill 	Bug 	Poison 	495 	65 	150 	40 	15 	80 	145 	1 	False
    16 	Pidgey 	Normal 	Flying 	251 	40 	45 	40 	35 	35 	56 	1 	False
    17 	Pidgeotto 	Normal 	Flying 	349 	63 	60 	55 	50 	50 	71 	1 	False
    18 	Pidgeot 	Normal 	Flying 	479 	83 	80 	75 	70 	70 	101 	1 	False
    18 	PidgeotMega Pidgeot 	Normal 	Flying 	579 	83 	80 	80 	135 	80 	121 	1 	False
    19 	Rattata 	Normal 		253 	30 	56 	35 	25 	35 	72 	1 	False
    20 	Raticate 	Normal 		413 	55 	81 	60 	50 	70 	97 	1 	False
    21 	Spearow 	Normal 	Flying 	262 	40 	60 	30 	31 	31 	70 	1 	False
    22 	Fearow 	Normal 	Flying 	442 	65 	90 	65 	61 	61 	100 	1 	False
    23 	Ekans 	Poison 		288 	35 	60 	44 	40 	54 	55 	1 	False
    24 	Arbok 	Poison 		438 	60 	85 	69 	65 	79 	80 	1 	False
    25 	Pikachu 	Electric 		320 	35 	55 	40 	50 	50 	90 	1 	False
    26 	Raichu 	Electric 		485 	60 	90 	55 	90 	80 	110 	1 	False
    27 	Sandshrew 	Ground 		300 	50 	75 	85 	20 	30 	40 	1 	False
    28 	Sandslash 	Ground 		450 	75 	100 	110 	45 	55 	65 	1 	False
    29 	Nidoran♀ 	Poison 		275 	55 	47 	52 	40 	40 	41 	1 	False
    30 	Nidorina 	Poison 		365 	70 	62 	67 	55 	55 	56 	1 	False
    31 	Nidoqueen 	Poison 	Ground 	505 	90 	92 	87 	75 	85 	76 	1 	False
    32 	Nidoran♂ 	Poison 		273 	46 	57 	40 	40 	40 	50 	1 	False
    33 	Nidorino 	Poison 		365 	61 	72 	57 	55 	55 	65 	1 	False
    34 	Nidoking 	Poison 	Ground 	505 	81 	102 	77 	85 	75 	85 	1 	False
    35 	Clefairy 	Fairy 		323 	70 	45 	48 	60 	65 	35 	1 	False
    36 	Clefable 	Fairy 		483 	95 	70 	73 	95 	90 	60 	1 	False
    37 	Vulpix 	Fire 		299 	38 	41 	40 	50 	65 	65 	1 	False
    38 	Ninetales 	Fire 		505 	73 	76 	75 	81 	100 	100 	1 	False
    39 	Jigglypuff 	Normal 	Fairy 	270 	115 	45 	20 	45 	25 	20 	1 	False
    40 	Wigglytuff 	Normal 	Fairy 	435 	140 	70 	45 	85 	50 	45 	1 	False
    41 	Zubat 	Poison 	Flying 	245 	40 	45 	35 	30 	40 	55 	1 	False
    42 	Golbat 	Poison 	Flying 	455 	75 	80 	70 	65 	75 	90 	1 	False
    43 	Oddish 	Grass 	Poison 	320 	45 	50 	55 	75 	65 	30 	1 	False
    44 	Gloom 	Grass 	Poison 	395 	60 	65 	70 	85 	75 	40 	1 	False
    45 	Vileplume 	Grass 	Poison 	490 	75 	80 	85 	110 	90 	50 	1 	False
    46 	Paras 	Bug 	Grass 	285 	35 	70 	55 	45 	55 	25 	1 	False
    47 	Parasect 	Bug 	Grass 	405 	60 	95 	80 	60 	80 	30 	1 	False
    48 	Venonat 	Bug 	Poison 	305 	60 	55 	50 	40 	55 	45 	1 	False
    49 	Venomoth 	Bug 	Poison 	450 	70 	65 	60 	90 	75 	90 	1 	False
    50 	Diglett 	Ground 		265 	10 	55 	25 	35 	45 	95 	1 	False
    51 	Dugtrio 	Ground 		405 	35 	80 	50 	50 	70 	120 	1 	False
    52 	Meowth 	Normal 		290 	40 	45 	35 	40 	40 	90 	1 	False
    53 	Persian 	Normal 		440 	65 	70 	60 	65 	65 	115 	1 	False
    54 	Psyduck 	Water 		320 	50 	52 	48 	65 	50 	55 	1 	False
    55 	Golduck 	Water 		500 	80 	82 	78 	95 	80 	85 	1 	False
    56 	Mankey 	Fighting 		305 	40 	80 	35 	35 	45 	70 	1 	False
    57 	Primeape 	Fighting 		455 	65 	105 	60 	60 	70 	95 	1 	False
    58 	Growlithe 	Fire 		350 	55 	70 	45 	70 	50 	60 	1 	False
    59 	Arcanine 	Fire 		555 	90 	110 	80 	100 	80 	95 	1 	False
    60 	Poliwag 	Water 		300 	40 	50 	40 	40 	40 	90 	1 	False
    61 	Poliwhirl 	Water 		385 	65 	65 	65 	50 	50 	90 	1 	False
    62 	Poliwrath 	Water 	Fighting 	510 	90 	95 	95 	70 	90 	70 	1 	False
    63 	Abra 	Psychic 		310 	25 	20 	15 	105 	55 	90 	1 	False
    64 	Kadabra 	Psychic 		400 	40 	35 	30 	120 	70 	105 	1 	False
    65 	Alakazam 	Psychic 		500 	55 	50 	45 	135 	95 	120 	1 	False
    65 	AlakazamMega Alakazam 	Psychic 		590 	55 	50 	65 	175 	95 	150 	1 	False
    66 	Machop 	Fighting 		305 	70 	80 	50 	35 	35 	35 	1 	False
    67 	Machoke 	Fighting 		405 	80 	100 	70 	50 	60 	45 	1 	False
    68 	Machamp 	Fighting 		505 	90 	130 	80 	65 	85 	55 	1 	False
    69 	Bellsprout 	Grass 	Poison 	300 	50 	75 	35 	70 	30 	40 	1 	False
    70 	Weepinbell 	Grass 	Poison 	390 	65 	90 	50 	85 	45 	55 	1 	False
    71 	Victreebel 	Grass 	Poison 	490 	80 	105 	65 	100 	70 	70 	1 	False
    72 	Tentacool 	Water 	Poison 	335 	40 	40 	35 	50 	100 	70 	1 	False
    73 	Tentacruel 	Water 	Poison 	515 	80 	70 	65 	80 	120 	100 	1 	False
    74 	Geodude 	Rock 	Ground 	300 	40 	80 	100 	30 	30 	20 	1 	False
    75 	Graveler 	Rock 	Ground 	390 	55 	95 	115 	45 	45 	35 	1 	False
    76 	Golem 	Rock 	Ground 	495 	80 	120 	130 	55 	65 	45 	1 	False
    77 	Ponyta 	Fire 		410 	50 	85 	55 	65 	65 	90 	1 	False
    78 	Rapidash 	Fire 		500 	65 	100 	70 	80 	80 	105 	1 	False
    79 	Slowpoke 	Water 	Psychic 	315 	90 	65 	65 	40 	40 	15 	1 	False
    80 	Slowbro 	Water 	Psychic 	490 	95 	75 	110 	100 	80 	30 	1 	False
    80 	SlowbroMega Slowbro 	Water 	Psychic 	590 	95 	75 	180 	130 	80 	30 	1 	False
    81 	Magnemite 	Electric 	Steel 	325 	25 	35 	70 	95 	55 	45 	1 	False
    82 	Magneton 	Electric 	Steel 	465 	50 	60 	95 	120 	70 	70 	1 	False
    83 	Farfetch'd 	Normal 	Flying 	352 	52 	65 	55 	58 	62 	60 	1 	False
    84 	Doduo 	Normal 	Flying 	310 	35 	85 	45 	35 	35 	75 	1 	False
    85 	Dodrio 	Normal 	Flying 	460 	60 	110 	70 	60 	60 	100 	1 	False
    86 	Seel 	Water 		325 	65 	45 	55 	45 	70 	45 	1 	False
    87 	Dewgong 	Water 	Ice 	475 	90 	70 	80 	70 	95 	70 	1 	False
    88 	Grimer 	Poison 		325 	80 	80 	50 	40 	50 	25 	1 	False
    89 	Muk 	Poison 		500 	105 	105 	75 	65 	100 	50 	1 	False
    90 	Shellder 	Water 		305 	30 	65 	100 	45 	25 	40 	1 	False
    91 	Cloyster 	Water 	Ice 	525 	50 	95 	180 	85 	45 	70 	1 	False
    92 	Gastly 	Ghost 	Poison 	310 	30 	35 	30 	100 	35 	80 	1 	False
    93 	Haunter 	Ghost 	Poison 	405 	45 	50 	45 	115 	55 	95 	1 	False
    94 	Gengar 	Ghost 	Poison 	500 	60 	65 	60 	130 	75 	110 	1 	False
    94 	GengarMega Gengar 	Ghost 	Poison 	600 	60 	65 	80 	170 	95 	130 	1 	False
    95 	Onix 	Rock 	Ground 	385 	35 	45 	160 	30 	45 	70 	1 	False
    96 	Drowzee 	Psychic 		328 	60 	48 	45 	43 	90 	42 	1 	False
    97 	Hypno 	Psychic 		483 	85 	73 	70 	73 	115 	67 	1 	False
    98 	Krabby 	Water 		325 	30 	105 	90 	25 	25 	50 	1 	False
    99 	Kingler 	Water 		475 	55 	130 	115 	50 	50 	75 	1 	False
    100 	Voltorb 	Electric 		330 	40 	30 	50 	55 	55 	100 	1 	False
    101 	Electrode 	Electric 		480 	60 	50 	70 	80 	80 	140 	1 	False
    102 	Exeggcute 	Grass 	Psychic 	325 	60 	40 	80 	60 	45 	40 	1 	False
    103 	Exeggutor 	Grass 	Psychic 	520 	95 	95 	85 	125 	65 	55 	1 	False
    104 	Cubone 	Ground 		320 	50 	50 	95 	40 	50 	35 	1 	False
    105 	Marowak 	Ground 		425 	60 	80 	110 	50 	80 	45 	1 	False
    106 	Hitmonlee 	Fighting 		455 	50 	120 	53 	35 	110 	87 	1 	False
    107 	Hitmonchan 	Fighting 		455 	50 	105 	79 	35 	110 	76 	1 	False
    108 	Lickitung 	Normal 		385 	90 	55 	75 	60 	75 	30 	1 	False
    109 	Koffing 	Poison 		340 	40 	65 	95 	60 	45 	35 	1 	False
    110 	Weezing 	Poison 		490 	65 	90 	120 	85 	70 	60 	1 	False
    111 	Rhyhorn 	Ground 	Rock 	345 	80 	85 	95 	30 	30 	25 	1 	False
    112 	Rhydon 	Ground 	Rock 	485 	105 	130 	120 	45 	45 	40 	1 	False
    113 	Chansey 	Normal 		450 	250 	5 	5 	35 	105 	50 	1 	False
    114 	Tangela 	Grass 		435 	65 	55 	115 	100 	40 	60 	1 	False
    115 	Kangaskhan 	Normal 		490 	105 	95 	80 	40 	80 	90 	1 	False
    115 	KangaskhanMega Kangaskhan 	Normal 		590 	105 	125 	100 	60 	100 	100 	1 	False
    116 	Horsea 	Water 		295 	30 	40 	70 	70 	25 	60 	1 	False
    117 	Seadra 	Water 		440 	55 	65 	95 	95 	45 	85 	1 	False
    118 	Goldeen 	Water 		320 	45 	67 	60 	35 	50 	63 	1 	False
    119 	Seaking 	Water 		450 	80 	92 	65 	65 	80 	68 	1 	False
    120 	Staryu 	Water 		340 	30 	45 	55 	70 	55 	85 	1 	False
    121 	Starmie 	Water 	Psychic 	520 	60 	75 	85 	100 	85 	115 	1 	False
    122 	Mr. Mime 	Psychic 	Fairy 	460 	40 	45 	65 	100 	120 	90 	1 	False
    123 	Scyther 	Bug 	Flying 	500 	70 	110 	80 	55 	80 	105 	1 	False
    124 	Jynx 	Ice 	Psychic 	455 	65 	50 	35 	115 	95 	95 	1 	False
    125 	Electabuzz 	Electric 		490 	65 	83 	57 	95 	85 	105 	1 	False
    126 	Magmar 	Fire 		495 	65 	95 	57 	100 	85 	93 	1 	False
    127 	Pinsir 	Bug 		500 	65 	125 	100 	55 	70 	85 	1 	False
    127 	PinsirMega Pinsir 	Bug 	Flying 	600 	65 	155 	120 	65 	90 	105 	1 	False
    128 	Tauros 	Normal 		490 	75 	100 	95 	40 	70 	110 	1 	False
    129 	Magikarp 	Water 		200 	20 	10 	55 	15 	20 	80 	1 	False
    130 	Gyarados 	Water 	Flying 	540 	95 	125 	79 	60 	100 	81 	1 	False
    130 	GyaradosMega Gyarados 	Water 	Dark 	640 	95 	155 	109 	70 	130 	81 	1 	False
    131 	Lapras 	Water 	Ice 	535 	130 	85 	80 	85 	95 	60 	1 	False
    132 	Ditto 	Normal 		288 	48 	48 	48 	48 	48 	48 	1 	False
    133 	Eevee 	Normal 		325 	55 	55 	50 	45 	65 	55 	1 	False
    134 	Vaporeon 	Water 		525 	130 	65 	60 	110 	95 	65 	1 	False
    135 	Jolteon 	Electric 		525 	65 	65 	60 	110 	95 	130 	1 	False
    136 	Flareon 	Fire 		525 	65 	130 	60 	95 	110 	65 	1 	False
    137 	Porygon 	Normal 		395 	65 	60 	70 	85 	75 	40 	1 	False
    138 	Omanyte 	Rock 	Water 	355 	35 	40 	100 	90 	55 	35 	1 	False
    139 	Omastar 	Rock 	Water 	495 	70 	60 	125 	115 	70 	55 	1 	False
    140 	Kabuto 	Rock 	Water 	355 	30 	80 	90 	55 	45 	55 	1 	False
    141 	Kabutops 	Rock 	Water 	495 	60 	115 	105 	65 	70 	80 	1 	False
    142 	Aerodactyl 	Rock 	Flying 	515 	80 	105 	65 	60 	75 	130 	1 	False
    142 	AerodactylMega Aerodactyl 	Rock 	Flying 	615 	80 	135 	85 	70 	95 	150 	1 	False
    143 	Snorlax 	Normal 		540 	160 	110 	65 	65 	110 	30 	1 	False
    144 	Articuno 	Ice 	Flying 	580 	90 	85 	100 	95 	125 	85 	1 	True
    145 	Zapdos 	Electric 	Flying 	580 	90 	90 	85 	125 	90 	100 	1 	True
    146 	Moltres 	Fire 	Flying 	580 	90 	100 	90 	125 	85 	90 	1 	True
    147 	Dratini 	Dragon 		300 	41 	64 	45 	50 	50 	50 	1 	False
    148 	Dragonair 	Dragon 		420 	61 	84 	65 	70 	70 	70 	1 	False
    149 	Dragonite 	Dragon 	Flying 	600 	91 	134 	95 	100 	100 	80 	1 	False
    150 	Mewtwo 	Psychic 		680 	106 	110 	90 	154 	90 	130 	1 	True
    150 	MewtwoMega Mewtwo X 	Psychic 	Fighting 	780 	106 	190 	100 	154 	100 	130 	1 	True
    150 	MewtwoMega Mewtwo Y 	Psychic 		780 	106 	150 	70 	194 	120 	140 	1 	True
    151 	Mew 	Psychic 		600 	100 	100 	100 	100 	100 	100 	1 	False
    152 	Chikorita 	Grass 		318 	45 	49 	65 	49 	65 	45 	2 	False
    153 	Bayleef 	Grass 		405 	60 	62 	80 	63 	80 	60 	2 	False
    154 	Meganium 	Grass 		525 	80 	82 	100 	83 	100 	80 	2 	False
    155 	Cyndaquil 	Fire 		309 	39 	52 	43 	60 	50 	65 	2 	False
    156 	Quilava 	Fire 		405 	58 	64 	58 	80 	65 	80 	2 	False
    157 	Typhlosion 	Fire 		534 	78 	84 	78 	109 	85 	100 	2 	False
    158 	Totodile 	Water 		314 	50 	65 	64 	44 	48 	43 	2 	False
    159 	Croconaw 	Water 		405 	65 	80 	80 	59 	63 	58 	2 	False
    160 	Feraligatr 	Water 		530 	85 	105 	100 	79 	83 	78 	2 	False
    161 	Sentret 	Normal 		215 	35 	46 	34 	35 	45 	20 	2 	False
    162 	Furret 	Normal 		415 	85 	76 	64 	45 	55 	90 	2 	False
    163 	Hoothoot 	Normal 	Flying 	262 	60 	30 	30 	36 	56 	50 	2 	False
    164 	Noctowl 	Normal 	Flying 	442 	100 	50 	50 	76 	96 	70 	2 	False
    165 	Ledyba 	Bug 	Flying 	265 	40 	20 	30 	40 	80 	55 	2 	False
    166 	Ledian 	Bug 	Flying 	390 	55 	35 	50 	55 	110 	85 	2 	False
    167 	Spinarak 	Bug 	Poison 	250 	40 	60 	40 	40 	40 	30 	2 	False
    168 	Ariados 	Bug 	Poison 	390 	70 	90 	70 	60 	60 	40 	2 	False
    169 	Crobat 	Poison 	Flying 	535 	85 	90 	80 	70 	80 	130 	2 	False
    170 	Chinchou 	Water 	Electric 	330 	75 	38 	38 	56 	56 	67 	2 	False
    171 	Lanturn 	Water 	Electric 	460 	125 	58 	58 	76 	76 	67 	2 	False
    172 	Pichu 	Electric 		205 	20 	40 	15 	35 	35 	60 	2 	False
    173 	Cleffa 	Fairy 		218 	50 	25 	28 	45 	55 	15 	2 	False
    174 	Igglybuff 	Normal 	Fairy 	210 	90 	30 	15 	40 	20 	15 	2 	False
    175 	Togepi 	Fairy 		245 	35 	20 	65 	40 	65 	20 	2 	False
    176 	Togetic 	Fairy 	Flying 	405 	55 	40 	85 	80 	105 	40 	2 	False
    177 	Natu 	Psychic 	Flying 	320 	40 	50 	45 	70 	45 	70 	2 	False
    178 	Xatu 	Psychic 	Flying 	470 	65 	75 	70 	95 	70 	95 	2 	False
    179 	Mareep 	Electric 		280 	55 	40 	40 	65 	45 	35 	2 	False
    180 	Flaaffy 	Electric 		365 	70 	55 	55 	80 	60 	45 	2 	False
    181 	Ampharos 	Electric 		510 	90 	75 	85 	115 	90 	55 	2 	False
    181 	AmpharosMega Ampharos 	Electric 	Dragon 	610 	90 	95 	105 	165 	110 	45 	2 	False
    182 	Bellossom 	Grass 		490 	75 	80 	95 	90 	100 	50 	2 	False
    183 	Marill 	Water 	Fairy 	250 	70 	20 	50 	20 	50 	40 	2 	False
    184 	Azumarill 	Water 	Fairy 	420 	100 	50 	80 	60 	80 	50 	2 	False
    185 	Sudowoodo 	Rock 		410 	70 	100 	115 	30 	65 	30 	2 	False
    186 	Politoed 	Water 		500 	90 	75 	75 	90 	100 	70 	2 	False
    187 	Hoppip 	Grass 	Flying 	250 	35 	35 	40 	35 	55 	50 	2 	False
    188 	Skiploom 	Grass 	Flying 	340 	55 	45 	50 	45 	65 	80 	2 	False
    189 	Jumpluff 	Grass 	Flying 	460 	75 	55 	70 	55 	95 	110 	2 	False
    190 	Aipom 	Normal 		360 	55 	70 	55 	40 	55 	85 	2 	False
    191 	Sunkern 	Grass 		180 	30 	30 	30 	30 	30 	30 	2 	False
    192 	Sunflora 	Grass 		425 	75 	75 	55 	105 	85 	30 	2 	False
    193 	Yanma 	Bug 	Flying 	390 	65 	65 	45 	75 	45 	95 	2 	False
    194 	Wooper 	Water 	Ground 	210 	55 	45 	45 	25 	25 	15 	2 	False
    195 	Quagsire 	Water 	Ground 	430 	95 	85 	85 	65 	65 	35 	2 	False
    196 	Espeon 	Psychic 		525 	65 	65 	60 	130 	95 	110 	2 	False
    197 	Umbreon 	Dark 		525 	95 	65 	110 	60 	130 	65 	2 	False
    198 	Murkrow 	Dark 	Flying 	405 	60 	85 	42 	85 	42 	91 	2 	False
    199 	Slowking 	Water 	Psychic 	490 	95 	75 	80 	100 	110 	30 	2 	False
    200 	Misdreavus 	Ghost 		435 	60 	60 	60 	85 	85 	85 	2 	False '''    
    df = pd.read_csv(StringIO(csv_str),sep='\t')
    #df.iloc[:,-1] = df.iloc[:,-1].fillna('')
    return df
pokemon_df = __create_dataframe2()






