import requests 
import json
import ast
import re
from pandas.core.frame import DataFrame 
import tweepy 
import nltk
import pandas as pd
import numpy as np
import seaborn as sns
import spacy
import string
import collections
import matplotlib.pyplot as plt
import en_core_web_sm
from wordcloud import WordCloud,STOPWORDS
nltk.download('punkt')   
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from tweepy import OAuthHandler 
from textblob import TextBlob
from bs4 import BeautifulSoup
from string import punctuation
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score


#########################################################################################################

url = ('https://newsapi.org/v2/top-headlines?'
       'sortBy=popularity&'
       'sources=bbc-news&'
       'apiKey=f9499a1f863d485d90d0ff3e820d6d2a')

response = requests.get(url)

nlp = en_core_web_sm.load() 
tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
stop = set(stopwords.words('english'))
punctuation = list(string.punctuation) #already taken care of with the cleaning function.
stop.update(punctuation)
w_tokenizer = WhitespaceTokenizer()




def furnished(text):
    final_text = []
    for i in w_tokenizer.tokenize(text):
       if i.lower() not in stop:
        word = lemmatizer.lemmatize(i)
        final_text.append(word.lower())
    return " " .join(final_text)


def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)


############################################################################################################################



def sentimentanalysis(df1):
    
    polarity=0

    positive=0
    negative=0
    neutral=0
    for i in range(df1.shape[0]):

        analysis = TextBlob(df1.iat[i,0])      #main sentiment analysis
        article_polarity=analysis.sentiment.polarity#main sentiment analysis

        if(article_polarity>0.00):
            #positive+=1
            articlepostsentiment.append((df1.iat[i,0],df1.iat[i,1],df1.iat[i,2],article_polarity,'positive'))
        elif(article_polarity<0.00):
            #negative+=1
            articlepostsentiment.append((df1.iat[i,0],df1.iat[i,1],df1.iat[i,2],article_polarity,'negative'))
        elif(article_polarity==0.00):
            #neutral+=1
            articlepostsentiment.append((df1.iat[i,0],df1.iat[i,1],df1.iat[i,2],article_polarity,'neutral'))
        #polarity += analysis.polarity
        #print(final_text)
    #print(polarity)
    #print(f'Amount of positive tweets:{positive}')
    #print(f'Amount of negative tweets:{negative}')
    #print(f'Amount of neutral tweets:{neutral}')
    
    df=pd.DataFrame(articlepostsentiment,columns=['Description','Raw Article','Article post-processing','polarity','sentiment analysis'])
    df=df.drop_duplicates(subset='Article post-processing')
    #df.to_csv('sentimentanalysis.csv',index=False)
    # return tweetsfinalpostsentiment
    return df

##############################################################################################

business_rel = '''business work company finance industry active marketing corporate financial engaged first occupy occupied fancy enterprise fussy officious accounting meddling personal profitable businesses busybodied job management interfering correspondence investment customer product person meddlesome sales professional entrepreneurial home business commercial tech government retail career companies econ corporation money in use brand retailing industrial biz property profitability technology e commerce people political businessperson office laboring service franchising entrepreneur commerce family formal labouring market organization economics toiling intrusive economy b2b school diligent entrepreneurial spirit legal manager casual enterprises building life entrepreneurs store economic house friend social restaurant profitably data overbusy admin business process outsourcing project operations entrepreneurship rush hour drudging friends tax industries law platform engineering wholesaling consumer startup website residential hobby ventures shop businesspeople clients income team technical side stem crowded politics employer private the employment core competency science owner medium sized businesses real estate client history class working customers land leasing corporations jobs public boss tied up individual investments tourist name at work media self farm up to rental analyst revenue tribute sme consulting ecommerce supply chain profit firms stock ebusiness marketplace investing manufacturing managers transactional smart investor production idea outsourcing suppliers analytics transaction creative education development profits congested medium enterprises domain quiet workforce brokerage tourism entity revenue streams clientele core competencies real apartment entertainment banking ceo contract medium sized productivity innovation smes employee not holiday site mid sized aspiring entrepreneurs value proposition app leadership artist franchisors growth markets sector shopping firm small business idle transactions medium sized enterprises innovate franchisee b2c startups networking employed freelance franchisees occupation supply chains putter labor profession potter dabble doing operation smatter occupational staying streets walking bustling traveling outside moving running workplace close turning train watching traffic stops downtown bus employ walk heading commuters through stop across sidewalk started lot neighborhood talking way going away stopped lots trouble stopping looking along busyness getting fast travelling morning around shops roads start coming room gone entering parking weekends seeing malls few go errands places scene street downstairs trips where quietly rush shoppers regularly opened things passing night just evening inside kept folks door sidewalks road hours besides leaving stroll concentrating ride everything out constantly setting keeping everyone labour workpiece collaborate overwork housewifery hire operative worker toil workly toiler task workable feasible retiree awork workful teamwork play around 're lifework vocation coursework rework erg ironwork workgroup drudge taskwork nonworking interwork taskmaster inwork employable weisure workfellow coworker openwork moil workling prework workfree jobshare yakka practicable lacework workcamp allwork businesslike bework benchwork bushwork skimp practical sourcework spadework paperwork labwork gridwork workstead swink workshed underwork stuccowork idleness ssp leatherwork metalwork groupwork shiftwork labourism copperworks workhouse exploit worklist fieldwork masterpiece brassworks postwork timberwork pairwork fink slave repertory patchwork unworked workmate troupe drudgery engage undertake hyperactive volunteer workflow clerical nightwork workshirt nonworker pitchwork subcontract lacquerware impermanent wirework silverwork cobwork charmwork handworked hectic gardenwork fond stressful spick adept tedious eventful careful exhausting overworked tired frantic brisk frenetic vigilant festive chatty challenging happy frustrating tough sleepy punctual tiresome anxious tricky mundane nosy clogged uneventful cautious'''
technology_rel = '''internet computer science technological engineering tech software computing systems application robotics electronics nanotechnology high technology biotechnology communication automation devices code game information innovations applications equipment tools technology virtual industry wireless computers hardware digital micro high tech robots solutions social phones media skill app knowledge bionics process business power machinery system products platform core computer science technological innovations nanotech product intelligence cyberscience society technical history electron commercial manufacturing screens ergonomics concept energy capability financial miniaturization electronic value developer labs build innovate nuclear weapon radio resources magic technician math guns club dynamic capabilities telephone development device aeronautical engineering ability technological advancements life cybersecurity revolutionize weapons industrial revolution makers systematics computer software nano mechanical engineer biomedical design materials scientific method programming language infrastructure phone framework human skills space medical services physics online world inventions ecosystem networked engine weapon screen programs reasoned formality multimedia cyberculture consumer military technology useful arts alchemy complicate sysop system science techniques hi tech proprietary medicine tool time technological advancement data production weaponry company information technology security understanding scientific wheel powers project handheld devices industrial machine second industrial revolution market progress growth applied science modern engineer games invention new video network coding grid computing apps methodology value proposition strategy pollution functionality subject study crowbar spoon mathematics developing communications global enterprise uses enabled focused processing mobile program generation aims networks economic globalization conspicuous leisure automotive technology computer technology electrical engineering industrial engineering industrial management subject area technologists biometrics climatology industrial arts informatics silk sedentism transmutation antiscience pulley cybernetics agronomy clock mutate physic environmental mining liberalize skyscraper television airplane australopithecus afarensis techie industrialize transistor professionalize inactivate satellite scientific discipline social science technologic tecnology research field of study technologically photonics technique nanotechnologies methods gaming digital imaging technological innovation civilization transhumanism machines biology rapidly evolving architecture innovating quality people management commercializing chemical engineering technologically advanced advancements domain expertise technologies electricity processes material protocol military comfort architectures core competencies scientific breakthroughs training projects bioscience rfid safety implementation breakthroughs scalable economic efficiency stack innovation composite materials 3d visualization gadgets languages solution neolithic tech gadgets arms things artifacts user interfaces cloud computing technological advances innovative agriculture construction biological source prehistory field lever marketing companies learning evolution algorithms metallurgy chemistry discipline bioengineering rocketry sink primates neo-luddism techno-progressivism phenomenal developed utility merriam-webster integrated advanced semiconductor based telecommunications sophisticated state-of-the-art components improve create expand creative enables component specialized wood neolithic revolution genome clothing goal-oriented nomad uruk sumer hierarchy irrigation pseudoscience neuroscience bellows furnace efficient energy use scientifically smelting human condition metrology practical application communications technology civil engineering flood control automotive engineering rail technology nuclear engineering mechanical engineering naval engineering alloys bronze brass imaging steel thorstein veblen microelectronics sociology biophysics bionanoscience technologies of the self modernize alchemical ursula franklin innovators evolutionary tribology transformation bernard stiegler phrenology technoscience superscience technics and time, 1 optimization horseshoe diagnostics microscopy multiscience geophysics space station proscience transformational demography particle accelerator organon psychology conversion scienceless telematics ic screw chasten geoscience business method metamorphosis converter fortran architectonics wheelbarrow sciencelike transformer radiography transmute methodologies glycoscience ize convert'''
politics_rel = '''political government law politician governance diplomatic polity political opportunism public administration diplomatical partisanship republic local government politics election aristotle politically political science partisan politics economics state ideologies politic religion politicking policy smooth debate wars politicians suave politicos nationalism values regionalism news democratic political system political expediency monarchy activism expedient geopolitics parliament culture history police republicanism morality ethics policies sagacious politicizing demagoguery elections electoral ban dynamics polis principle international politics governor sociopolitical judiciary resourceful mudslinging social pragmatism policymaking body politic drama divisive divisiveness factionalism ideological statecraft parochialism cynicism society gubernatorial world populism regime issues partisan bickering pandering religious populist conspiracy international human money science federal government rhetoric bureaucracy intrigue personal democracy identity warfare force ideas tribes controversial united nations allegiance civil celibacy commerce civilised sinfulness stuffy meddles unclothed crystallizing psyche policy-making latinisation of names clubby metabolizes political parties crafty minimalist issue realpolitik crist demagogue supremacy the wealth of nations politick statesmanship conservatism electioneering electorate idealism dukes journalism sovereign state mud slinging tribalism current partisan business philosophy sleaze pettiness beliefs ideology race economy power chauvinism machinations public affairs campaigning events voting people diplomacy laws demagogues sloganeering opinions military optics legislating communism self aggrandizement obstructionism federation agendas sociology relations anarchism agenda aristocracy bland governments racism gov tribe propaganda party civics cultural econ city company plato corporate system opinion confucius kingship other counts earls capitalism foreign strategy morals tribute property education community finance comedy politicized inheritance manifesto legislation legal action worldview confiscation lawmaking individualist management woke congress problems trade control conflict global ideals meta virtue justice espionage treason how health lack games actions factions personality behavior convention gentile observance taxation petition collegial majority greek language permeates permeating flabby communication governmental permeated pervades straitjacket discourse abstract civilization curfew discernment consciences pervading matriarchal rightness juridical unaccountable transfigured monopoly deliberative paternalism coin perverted permeate subjectivity enmeshed transitory cesspool guild disinterested fleshly redefining egoism quicksand diplomat peculiarly agreement colonies ancient greek early modern english profit modern english decisionmaking middle french anarchy liberalism engrained executive pols colorblind humorless art of warfare downshifting psychodrama balkanized self-perpetuating internalised reflation divine right of kings kafkaesque nontransparent democracies postindustrial unsustainability democrat atomized overregulated privy council socialism self-regulating oligarchies nonideological hidebound constitutional monarchy wrongness dispassion tyrannies constitutional government heteronormative soviet depersonalized corporatism covenantal shapers microbiota originalism solipsistic seven-man presidency standard-setting empowerment groupthink eviscerated sovereignty autocracy 146-nation president constitutions military service imperialism restoration privatization sly apolitical presidential interpol preside france mastermind elites racketeer federal australia campaigner cunning contract criminal law administrative confederation ombudsman private law generalissimo position officer wily senator trial by jury ceo democrats financier autocratic secede protestant reformation anarchist timocracy drunk driving manipulative globalization posturing political representation artifice suzerainty bloc politicize shrewd multinational warden politricks privatize federalization dishonest tenderpreneur govern authority treasurer separatism statesperson expert chancellor economist guile commissioner impolitic neocolonialism papacy politik chomsky religio hegelian theo quietism parliamentary circumlocution roguery sayers moralize bonapartist religionist reactionary pragmatics egotistic raison contestation enlightened poli viler intelligentsia jurisdiction hausa cabal manipulation shrewdness controller official corporatist wizard socialist supervision dominion organisation skillful party system cleverness'''
sports_rel = '''football activities soccer athletics racing gymnastics sportsman games baseball spectator sport cycling tennis game hockey competition rugby union entertainment association football basketball fitness hobbies esports exercise athletic rugby clubs luxury downfield gym muscle judo offside super skiing physical team polo music rowing school fun sportswoman play news events volleyball leagues wrestling professional sport action concert concerts run work call athlete party kill martial spar professional basketball ineligible hobby wildlife referee teams golf gaming badminton schuss luge gyms activity athletes documents team sport blood sport social sports working athletic game video media water television intramurals upfield beach volleyball jocularity cheerlead championship olympic sport soccerball archery club professional football outdoors other contact sport training toboggan top wii funambulism movies dance bra ortho car workout professional baseball gambling shows running bobsled dive casino personal foul race recreational riding outdoor sport wipeout movie skateboard outdoor skating celebrity health performance jackknife arts speed skate supercars bralette hunting ski cars the event extra fighting recreation competitions comedy figure skate resort celebrities physio culture pokemon rollerblade college exercises pop roller skate espn casual ice skate leisure hiking lifting tops politics show medical cultural regulation time blazer nfl extracurriculars mutation extracurricular boast sport art mma bralettes restaurant frolic competitive lark business supercar life bras binder compression skylark frisk feature gambol gatorade orthopedic mutant disport physical activity romp active camping romance political band energy pub bar academic coach daisy cutter olympics bally rec rollick boxing cavort etc fantasy societies touring cricket water ski track tool trading leggings sporting events sudden death lark about sportsperson run around motocross swimming sumo intramural sports coaches sportswriters sportswriter enthusiasts sportsmanship mixed martial arts pastime hoops chess intercollegiate athletics shooter playing players downhill skiing sportspeople position sportaccord stadiums watersports golfing equestrianism sporting sporting goods sportsmen olympic games job field home olympic popular models for concussion weightlifting cheerleading council of europe championships bmx racers challenge drag racing performing arts wakeboarding sports federations footie sportscaster bodybuilding ultimate frisbee gridiron broadcasting motorsport jocks amateur boxing bass fishing ice rinks telecasts aquatics lacrosse variation tournament summercater champion playoffs season nascar sportsbook dexterity athleticism foul handler jog defense box trial defence cut series english side canoe tuck dribble save bob possession shot stroke sledding equitation away row defending diversion pass toss occupation flip line paddle surf carry drive racket punt surfboard kick onside bandy submarine kayak down pack drop backpack umpire snorkel scull rappel shoot mountaineer curl start seed underarm clowning surge underhand turn round underhanded hurdle bout sleigh average overhand loose legal humor wit humour hike lead timer deficit witticism timekeeper disqualified scout sled ironman ref skate tramp manager softball sportive goal tradition dodgeball biathlon floorball overarm soccerplex jocosity waggishness windsurf wittiness skin-dive abseil prizefight double-team outclass overhanded birling shadowbox spread-eagle logrolling man-to-man offsides most-valuable one-on-one sportful waggery gameday sporter nonsports sportsaholic footballer multisport sportless outsport acrobatic lusorious sportlike powerlifting paddlesport rugger sportsplex go gamesome gaelic football postseason pickleball passtime professional kiteboarding slalom competing birle skateboarder sportling world racquet british english compete american english competes bowling'''
entertainment_rel = '''media music amusement recreation nightlife leisure infotainment theater storytelling game edutainment television fun sports multimedia gaming comedy tv cinema animation movies sport circus theatre film hollywood play art enjoyment extravaganza spectacle news entertainment industry drama show food marketing social movie cultural fashion broadcasting programming escapist arts banquet dance performance concert videogames info enrichment engagement insight competitive dance teasing handheld gaming digital content tech games beverage pop culture entertainment hospitality sporting events audio visual auditorium wholesome immersive rgf pleasure out opinion merchandising happiness epic scheherazade satire multiplatform dining performance poetry hobby running films bamboo nawab goryeo militainment culture chef cabaret meaning of life odyssey get entertain shopping information entertainments travel gaming console educational interactivity business restaurant distraction video gambling enlarge associated press streaming stand extravaganzas radio stadium celebrity advertising production service work creative hobbies education surround sound luxury retail online game acting restaurants pop shows eating pantomime activities events sporting stimulation consumer electronics lifestyle money outdoor recreation amusement rides socializing humor world war i propaganda shock fiction nav toys vaudeville tourism relaxation living idol artistic solo fantasy musical comedic comfort quality casual dining joy time entertained musician tourist personal gossip story experiential value discretionary digital signage robbie bach commercial electronics office interest ball sex recreational variety communication interactive ring tones internet consumer navigation life experience animatronics impresario cost toy wrestling watersports ancillary industry personality influencer commentary journalism talent meme slapstick preshow poker reality excitement modeling curiosity room activity bars mass entertain water knowledge exercise programing audience theatrical showbiz amenities escape meals audio world services court ceremony party professional opera fencing festival archery arcade anime dancing magic remix neologism gratification poetry audiobook novel diversion studios camping birthday ethics networks web theme entertainer corporate catering ticketing fraxinus jumping hickory horse racing hazel gladiator stilts multiplex carthage racing colosseum durbar museology schadenfreude maharaja commoner nautch shamanism jousting komnenos aristocracy beguilement tournament decapitation hanging stoning clown puppet cartoon productions network marble imagination vcr hbo cognition paramount rhythm boredom universal cable online abc nickelodeon jazz nbc studio amplifier cbs mtv choir orchestra channel viacom singing exclusive mgm themed tiltyard showtime miramax pbs warner espn monopoly go backgammon publishing channels llc theaters pharaoh showcase marketplace pictures religious festival tutankhamun walt mega outlets ticket whist feature based fox bingo owns airs dreamworks television show venture magazine blockbuster distributor co featured brand hide-and-seek piggy-back fi croquet video game ventures operates vh1 dvd paintball touchstone syndicated features music festival series film festival sudoku amusements reading literature font comics limerick superheroes william shakespeare audiovisual superman peanuts the matrix the hitchhiker's guide to the galaxy bros. radio comedy manga caricature night life entertainers adventure game lp record genre jester phrases from the hitchhiker's guide to the galaxy videogame insult beverages philosophical method buffoon senet dwarfism pole vault karaoke pun wit parody irony carbon-fiber-reinforced polymer farce roman empire masque publican hopscotch be entertain cultural revolution inc. revolutionary opera russian revolution great depression pilgrim music hall motorsports movie theater iran tablet computer orality you're bore wayang maya civilization gamelan mughal emperors british'''



business = furnished(business_rel)
technology = furnished(technology_rel)
politics = furnished(politics_rel)
sports = furnished(sports_rel)
entertainment = furnished(entertainment_rel)
string1 = business
#print(string1)
words=string1.split()
#print(words)
business = " ".join(sorted(set(words),key=words.index))
#print(economy)

string1 = technology
words=string1.split()
technology = " ".join(sorted(set(words),key=words.index))


string1 = politics
words=string1.split()
politics = " ".join(sorted(set(words),key=words.index))


string1 = sports
words=string1.split()
sports = " ".join(sorted(set(words),key=words.index))


string1 = entertainment
words=string1.split()
entertainment = " ".join(sorted(set(words),key=words.index))


def cluster_classification(df):
    articlefinalpostclassification=[]
    for i in range(df.shape[0]):
        b = jaccard_similarity(business, df.iat[i,2])
        t = jaccard_similarity(technology,  df.iat[i,2])
        p = jaccard_similarity(politics, df.iat[i,2])
        s = jaccard_similarity(sports,  df.iat[i,2])
        e = jaccard_similarity(entertainment,  df.iat[i,2])
        f = max(b,t,p,s,e)
        if(f>0.5):
            if(f==b):
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'Business',f))
            elif(f==t):
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'Technology',f))
            elif(f==p):
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'Politics',f))
            elif(f==s):
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'Sports',f))
            elif(f==e):
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'Entertainment',f))
        else:
                articlefinalpostclassification.append((df.iat[i,0],df.iat[i,1],df.iat[i,2],df.iat[i,3],df.iat[i,4],'None',f))
           
        #print(tweet+":")
        #print(s)
    return articlefinalpostclassification




############################################################################################


jsonstr = response.json()
#print(jsonstr)
articlepostprocessing = []
articlepostsentiment = []

for i in range(0,len(jsonstr['articles'])):
    description = jsonstr['articles'][i]['description']
    extrawarticle = jsonstr['articles'][i]['content']
    #print(extrawarticle)
    #rawarticle = rawarticle.text
    rawarticle = ''.join([c for c in extrawarticle if ord(c) < 128])#removing weird text
    rawarticle = BeautifulSoup(rawarticle,'lxml').get_text()#removes html tags
    rawarticle = ' '.join(re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", " ", rawarticle).split())#removing mentions and hashtags
    rawarticle = ' '.join(re.sub("http://\S+|https://\S+", " ", rawarticle).split())#removing links
    rawarticle = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", rawarticle).split())#removing punctuations
    rawarticle = rawarticle.lower()#converting to lower case
    article = furnished(rawarticle)
    articlepostprocessing.append((description,extrawarticle,article))
df1=pd.DataFrame(articlepostprocessing,columns=['Description','Raw Article','Article post-processing'])
print('Pre processing\n',df1.head())
df1 = df1.dropna()
df1=df1.drop_duplicates(subset='Article post-processing')
#df1.to_csv('preprocessing.csv',index=False)
articlefinalpostsentiment_df=sentimentanalysis(df1)
print('Post Sentiment\n',articlefinalpostsentiment_df)
twitterfinalpostclassification=cluster_classification(articlefinalpostsentiment_df)
df_combined=pd.DataFrame(twitterfinalpostclassification,columns=['Description','Raw Article','Article post-processing','polarity','sentiment analysis', 'category','Score' ])
df_combined=df_combined.drop_duplicates(subset='Article post-processing')
df_combined.to_csv('finaldata.csv',index=False)
print('Post Classification\n',df_combined)
#cont = response.content
#my_dict = json.loads(response.decode('utf-8'))
#for res in response['articles']:
#    prints(res.description)