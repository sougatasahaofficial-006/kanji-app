import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n1_part1.json"
PART2_JSON_PATH = "n1_part2.json"
PART3_JSON_PATH = "n1_part3.json"
PART4_JSON_PATH = "n1_part4.json"
OUTPUT_TS_PATH = os.path.join("src", "data", "n1.ts")

N1_PART5_DATA = [
    # Lesson 500[cite: 48]
    [
        ("鶴", "つる", "crane / stork", ["カク"], ["つる"]),
        ("埼", "さい", "cape / spit / promontory", ["キ"], ["さき"]),
        ("栃", "とち", "horse chestnut", [], ["とち"]),
        ("茨", "いばら", "briar / thorn / wild rose", ["シ", "ジ"], ["いばら"]),
        ("埼玉", "さいたま", "Saitama", [], ["さいたま"]),
    ],
    # Lesson 501[cite: 48]
    [
        ("阜", "ふ", "hill / mound / left village radical", ["フ", "フウ"], []),
        ("岐阜", "ぎふ", "Gifu", [], ["ぎふ"]),
        ("串", "くし", "spit / skewer", ["カン", "ケン", "セン"], ["くし"]),
        ("丼", "どんぶり", "porcelain bowl / bowl of rice with food on top", ["トン", "タン"], ["どんぶり"]),
        ("一服", "いっぷく", "a dose / a puff / a cup of tea / a short rest", ["イップク"], []),
    ],
    # Lesson 502[cite: 48]
    [
        ("乞う", "こう", "to beg / ask / request / implore", ["コツ", "キツ", "キ"], ["こ.う"]),
        ("侶", "りょ", "companion / follower", ["リョ", "ロ"], []),
        ("僧侶", "そうりょ", "priest / monk", ["ソウリョ"], []),
        ("傲", "ごう", "be proud / arrogant", ["ゴウ"], ["おご.る"]),
        ("乞食", "こじき", "beggar / panhandler", ["コジキ"], []),
    ],
    # Lesson 503[cite: 48]
    [
        ("傲慢", "ごうまん", "haughty / arrogant / insolent / proud", ["ゴウマン"], []),
        ("僅", "きん", "a wee bit", ["キン"], ["わず.か"]),
        ("冥", "めい", "dark / Hades / underworld", ["メイ", "ミョウ"], ["くら.い"]),
        ("冥利", "みょうり", "divine favor / luck / advantage", ["ミョウリ"], []),
        ("僅か", "わずか", "only / merely / a little / small quantity", ["キン"], ["わず.か"]),
    ],
    # Lesson 504[cite: 48]
    [
        ("刹", "せつ", "temple", ["セツ", "サツ"], []),
        ("剝く", "むく", "to peel / skin / pare / hull", ["ハク"], ["む.く", "む.ける"]),
        ("勅", "ちょく", "imperial order", ["チョク"], ["みことのり"]),
        ("勃発", "ぼっぱつ", "outbreak (e.g. war) / sudden occurrence", ["ボッパツ"], []),
        ("敷設", "ふせつ", "construction / laying (railroad, mine, cable)", ["フセツ"], []),
    ],
    # Lesson 505[cite: 48]
    [
        ("勾", "こう", "be bent / slope / capture", ["コウ", "ク"], ["かぎ", "ま.がる"]),
        ("勾配", "こうばい", "slope / incline / gradient / pitch", ["コウバイ"], []),
        ("呪", "じゅ", "spell / curse / charm / malediction", ["ジュ", "シュ"], ["のろ.う", "まじな.う"]),
        ("呪術", "じゅじゅつ", "magic / sorcery / incantation", ["ジュジュツ"], []),
        ("呪い", "のろい", "curse / spell / malediction", ["ジュ"], ["のろ.い"]),
    ],
    # Lesson 506[cite: 48]
    [
        ("咽", "いん", "throat / choked / smothered / stuffy", ["イン", "エツ"], ["むせ.ぶ", "のど"]),
        ("耳鼻咽喉科", "じびいんこうか", "otorhinolaryngology / ENT department", ["ジビインコウカ"], []),
        ("哺", "ほ", "nurse / suckle", ["ホ"], ["はぐく.む"]),
        ("哺乳類", "ほにゅうるい", "mammals / mammalian", ["ホニュウルイ"], []),
        ("捕鯨", "ほげい", "whaling", ["ホゲイ"], []),
    ],
    # Lesson 507[cite: 48]
    [
        ("喩", "ゆ", "metaphor / compare", ["ユ"], ["たと.える"]),
        ("比喩", "ひゆ", "simile / metaphor / allegory / parable", ["ヒユ"], []),
        ("嘲", "ちょう", "ridicule / insult", ["チョウ", "トウ"], ["あざけ.る"]),
        ("自嘲", "じちょう", "self-deprecation / self-scorn", ["ジチョウ"], []),
        ("慰安", "いあん", "solace / relaxation / recreation / comfort", ["イアン"], []),
    ],
    # Lesson 508[cite: 48]
    [
        ("堆", "たい", "piled high", ["タイ", "ツイ"], ["うずたか.い"]),
        ("堆肥", "たいひ", "compost / manure", ["タイヒ"], []),
        ("填", "てん", "fill in", ["テン", "チン"], ["は.まる", "は.める"]),
        ("妖", "よう", "attractive / bewitching / calamity", ["ヨウ"], ["あや.しい"]),
        ("盲目", "もうもく", "blindness", ["モウモク"], []),
    ],
    # Lesson 509[cite: 48]
    [
        ("妖怪", "ようかい", "ghost / apparition / phantom / monster", ["ヨウカイ"], []),
        ("嫉", "しつ", "jealous / envy", ["シツ"], ["そね.む", "ねた.む"]),
        ("嫉妬", "しっと", "jealousy / envy", ["シット"], []),
        ("彙", "い", "same kind / collect / classify / category", ["イ"], []),
        ("隠れ家", "かくれが", "hideout / refuge / retreat", [], ["かくれが"]),
    ],
    # Lesson 510[cite: 48]
    [
        ("語彙", "ごい", "vocabulary / lexicon / lexis / terminology", ["ゴイ"], []),
        ("怨ずる", "えんずる", "to bear a grudge / resent", ["エン", "オン"], ["えん.ずる"]),
        ("怨念", "おんねん", "deep-seated grudge / hatred", ["オンネン"], []),
        ("恣", "し", "selfish / arbitrary", ["シ"], ["ほしいまま"]),
        ("天皇陛下", "てんのうへいか", "His Majesty the Emperor", ["テンノウヘイカ"], []),
    ],
    # Lesson 511[cite: 48]
    [
        ("恣意", "しい", "arbitrariness / selfishness / wilfulness", ["シイ"], []),
        ("惧", "ぐ", "disquiet / fear", ["グ"], ["おそ.れる"]),
        ("危惧", "きぐ", "apprehension / fear / misgivings", ["キグ"], []),
        ("慄", "りつ", "fear", ["リツ"], ["おのの.く"]),
        ("芳香", "ほうこう", "perfume / fragrance / aroma / sweet smell", ["ホウコウ"], []),
    ],
    # Lesson 512[cite: 48]
    [
        ("戦慄", "せんりつ", "shudder / shiver / tremor", ["センリツ"], []),
        ("憬", "けい", "yearn after / long for / aspire to / admire", ["ケイ"], ["あこが.れる"]),
        ("憧憬", "どうけい", "longing / yearning / aspiration", ["ドウケイ", "ショウケイ"], []),
        ("拉", "ら", "latin / pull / crush / kidnap", ["ラ", "ラツ"], ["らっ.する"]),
        ("拉致", "らち", "taking captive / carrying away / kidnapping", ["ラチ"], []),
    ],
    # Lesson 513[cite: 48]
    [
        ("挫", "ざ", "crush / break / sprain / discourage", ["ザ"], ["くじ.く", "くじ.ける"]),
        ("挫折", "ざせつ", "setback / failure (e.g. plans) / frustration", ["ザセツ"], []),
        ("捉える", "とらえる", "to catch / capture / seize / arrest / grab", ["ソク"], ["とら.える"]),
        ("捗", "ちょく", "make progress", ["チョク", "ホ"], ["はかど.る"]),
        ("随筆", "ずいひつ", "essays / miscellaneous writings / literary jottings", ["ズイヒツ"], []),
    ],
    # Lesson 514[cite: 49]
    [
        ("捻", "ねん", "twirl / twist / wrench", ["ネン"], ["ね.じる", "ひね.る"]),
        ("摯", "し", "seriousness", ["シ"], []),
        ("真摯", "しんし", "sincere / earnest / serious", ["シンシ"], []),
        ("斑", "はん", "spot / blemish / speck / dapple", ["ハン"], ["ふ", "まだら"]),
        ("捻る", "ひねる", "to twist / wrench / turn (a switch on or off)", ["ネン"], ["ひね.る"]),
    ],
    # Lesson 515[cite: 49]
    [
        ("曾", "そう", "formerly / once / before / ever / never", ["ソウ", "ソ", "ゾウ"], ["かつ", "かつて"]),
        ("柵", "さく", "stockade / fence / weir / entanglements", ["サク", "サン"], ["しがらみ"]),
        ("柿", "かき", "persimmon", ["シ"], ["かき"]),
        ("桁", "けた", "beam / girder / spar / digit / order of magnitude", ["コウ"], ["けた"]),
        ("吹奏", "すいそう", "playing wind instruments", ["スイソウ"], []),
    ],
    # Lesson 516[cite: 49]
    [
        ("梗", "こう", "for the most part / close up / flower stem", ["コウ", "キョウ"], []),
        ("心筋梗塞", "しんきんこうそく", "myocardial infarction / heart attack", ["シンキンコウソク"], []),
        ("楷", "かい", "square character style / correctness", ["カイ"], []),
        ("楷書", "かいしょ", "square style (of kanji) / printed style", ["カイショ"], []),
        ("どん底", "どんぞこ", "very bottom / lowest depths", [], ["どんぞこ"]),
    ],
    # Lesson 517[cite: 49]
    [
        ("毀", "き", "break / destroy / censure / be chipped", ["キ"], ["こぼ.つ", "こわ.す"]),
        ("毀損", "きそん", "damage / injury / defamation / harm", ["キソン"], []),
        ("氾", "はん", "spread out / wide", ["ハン"], ["ひろ.がる"]),
        ("氾濫", "はんらん", "overflowing / flood / inundation / deluge", ["ハンラン"], []),
        ("蜂起", "ほうき", "uprising / revolt / insurrection", ["ホウキ"], []),
    ],
    # Lesson 518[cite: 49]
    [
        ("汎", "はん", "general / universal / pan-", ["ハン"], []),
        ("沃", "よく", "fertility", ["ヨク"], []),
        ("淫", "いん", "lewdness / licentiousness", ["イン"], ["みだ.ら", "みだ.れる"]),
        ("煎", "せん", "broil / parch / roast / boil", ["セン"], ["い.る", "せん.じる"]),
        ("下敷き", "したじき", "desk pad / underlay / being pinned under", [], ["したじき"]),
    ],
    # Lesson 519[cite: 49]
    [
        ("煎茶", "せんちゃ", "sencha (medium-grade green tea)", ["センチャ"], []),
        ("牙", "きば", "tusk / fang", ["ガ", "ゲ"], ["きば", "は"]),
        ("玩", "がん", "trifle with / play / take pleasure in", ["ガン"], ["もてあそ.ぶ"]),
        ("玩具", "おもちゃ", "toy / plaything", ["ガング"], ["おもちゃ"]),
        ("短冊", "たんざく", "tanzaku / small vertical paper strip for writing poems", ["タンザク"], []),
    ],
    # Lesson 520[cite: 49]
    [
        ("畏", "い", "fear / majestic / graciously / be apprehensive", ["イ"], ["おそ.れる", "かしこ.まる"]),
        ("畏敬", "いけい", "reverence / awe / respect", ["イケイ"], []),
        ("畿", "き", "capital / suburbs of capital", ["キ"], ["みやこ"]),
        ("近畿", "きんき", "Kinki (region around Osaka, Kyoto, Nara)", ["キンキ"], []),
        ("質素", "しっそ", "simplicity / modesty / frugality", ["シッソ"], []),
    ],
    # Lesson 521[cite: 49]
    [
        ("痕", "あと", "mark / print / impression / trace / evidence", ["コン"], ["あと"]),
        ("痕跡", "こんせき", "traces / marks / evidence / vestige", ["コンセキ"], []),
        ("瘍", "よう", "carbuncle / ulcer / sore / boil", ["ヨウ"], []),
        ("腫瘍", "しゅよう", "tumor / tumour / neoplasm", ["シュヨウ"], []),
        ("和やか", "なごやか", "mild / calm / gentle / quiet / harmonious", ["ワ"], ["なご.やか"]),
    ],
    # Lesson 522[cite: 49]
    [
        ("窟", "くつ", "cavern", ["クツ"], ["いわや"]),
        ("洞窟", "どうくつ", "cavern / cave / grotto", ["ドウクツ"], []),
        ("箋", "せん", "paper / label / letter / composition", ["セン"], []),
        ("処方箋", "しょほうせん", "prescription", ["ショホウセン"], []),
        ("払拭", "ふっしょく", "wiping out / sweeping away / eradication", ["フッショク"], []),
    ],
    # Lesson 523[cite: 49]
    [
        ("籠", "かご", "basket / cage", ["ロウ", "ル"], ["かご", "こ.もる"]),
        ("緻", "ち", "fine (not coarse)", ["チ"], []),
        ("精緻", "せいち", "minute / subtle / delicate / fine / elaborate", ["セイチ"], []),
        ("蓋", "ふた", "cover / lid / cap", ["ガイ"], ["ふた"]),
        ("紡績", "ぼうせき", "spinning (textiles)", ["ボウセキ"], []),
    ],
    # Lesson 524[cite: 49]
    [
        ("羞恥", "しゅうち", "shyness / bashfulness / shame", ["シュウチ"], []),
        ("羨", "せん", "envious / be jealous / covet", ["セン", "エン"], ["うらや.む"]),
        ("羨望", "せんぼう", "envy", ["センボウ"], []),
        ("脊", "せ", "stature / height / back / spine", ["セキ"], ["せ", "せい"]),
        ("羨ましい", "うらやましい", "envious / jealous", ["セン"], ["うらや.ましい"]),
    ],
    # Lesson 525[cite: 49]
    [
        ("脊椎", "せきつい", "spine / vertebral column", ["セキツイ"], []),
        ("腎", "じん", "kidney", ["ジン"], []),
        ("腎臓", "じんぞう", "kidney", ["ジンゾウ"], []),
        ("腺", "せん", "gland", ["セン"], []),
        ("脚光", "きゃっこう", "footlight / limelight / public attention", ["キャッコウ"], []),
    ],
    # Lesson 526[cite: 51]
    [
        ("甲状腺", "こうじょうせん", "thyroid gland", ["コウジョウセン"], []),
        ("臼", "うす", "mortar", ["キュウ"], ["うす"]),
        ("舷", "げん", "gunwale / side of a ship", ["ゲン"], ["ふなばた"]),
        ("右舷", "うげん", "starboard", ["ウゲン"], []),
        ("喝采", "かっさい", "applause / cheers / acclaim", ["カッサイ"], []),
    ],
    # Lesson 527[cite: 51]
    [
        ("萎", "い", "wither / droop / lame", ["イ"], ["な.える", "しぼ.む"]),
        ("萎縮", "いしゅく", "withering / atrophy / contraction / shrinking", ["イシュク"], []),
        ("葛", "くず", "arrowroot / kudzu", ["カツ"], ["くず", "つづら"]),
        ("蔽", "へい", "cover / shade / mantle / be ruined", ["ヘイ", "ヘツ", "フツ"], ["おお.う"]),
        ("葛藤", "かっとう", "conflict / complications / discord / strife", ["カットウ"], []),
    ],
    # Lesson 528[cite: 51]
    [
        ("訃", "ふ", "obituary", ["フ"], []),
        ("訃報", "ふほう", "news of someone's death / obituary", ["フホウ"], []),
        ("詣", "けい", "visit a temple", ["ケイ", "ゲイ"], ["けい.する", "まい.る"]),
        ("参詣", "さんけい", "visit to a shrine or temple / pilgrimage", ["サンケイ"], []),
        ("隠蔽", "いんぺい", "concealment / hiding / cover-up", ["インペイ"], []),
    ],
    # Lesson 529[cite: 51]
    [
        ("詮", "せん", "discussion / selection / result", ["セン"], ["せん.ずる", "かい"]),
        ("諧", "かい", "order / harmony", ["カイ"], ["かな.う", "やわ.らぐ"]),
        ("俳諧", "はいかい", "haikai / renku / humorous linked verse", ["ハイカイ"], []),
        ("貌", "ぼう", "form / appearance / countenance", ["ボウ", "バク"], ["かたち", "かたどる"]),
        ("所詮", "しょせん", "after all / in the end / anyway", ["ショセン"], []),
    ],
    # Lesson 530[cite: 51]
    [
        ("変貌", "へんぼう", "transfiguration / transformation / complete change", ["ヘンボウ"], []),
        ("貪", "どん", "covet / indulge in", ["ドン", "タン", "トン"], ["むさぼ.る"]),
        ("賂", "ろ", "bribe", ["ロ"], ["まいな.う", "まいない"]),
        ("賄賂", "わいろ", "bribe", ["ワイロ"], []),
        ("初詣", "はつもうで", "first shrine visit of the New Year", [], ["はつもうで"]),
    ],
    # Lesson 531[cite: 51]
    [
        ("踪", "そう", "remains / clue / footprint", ["ソウ"], ["あと"]),
        ("辣", "らつ", "bitter / pungent / harsh", ["ラツ"], ["から.い"]),
        ("遡", "そ", "go upstream / retrace the past", ["ソ", "サク"], ["さかのぼ.る"]),
        ("遡る", "さかのぼる", "to go upstream / go back (in time, to origin)", ["ソ"], ["さかのぼ.る"]),
        ("失踪", "しっそう", "disappearance / running away / absconding", ["シッソウ"], []),
    ],
    # Lesson 532[cite: 51]
    [
        ("酎", "ちゅう", "sake", ["チュウ", "チュ"], []),
        ("焼酎", "しょうちゅう", "shochu (Japanese distilled spirit)", ["ショウチュウ"], []),
        ("醒", "せい", "awake / be disillusioned / sober up", ["セイ"], ["さ.める", "さ.ます"]),
        ("覚醒剤", "かくせいざい", "stimulant (e.g. psychoactive drug)", ["カクセイザイ"], []),
        ("信奉", "しんぽう", "belief / adherence / faith", ["シンポウ"], []),
    ],
    # Lesson 533[cite: 51]
    [
        ("錮", "こ", "weld / tie / lock up", ["コ"], []),
        ("禁錮", "きんこ", "imprisonment (without forced labor)", ["キンコ"], []),
        ("頓", "とん", "suddenly / in a hurry / arrange / bow", ["トン", "トツ"], ["にわか.に"]),
        ("頬", "ほお", "cheek", ["キョウ"], ["ほお", "ほほ"]),
        ("逸品", "いっぴん", "gem / masterpiece / rare article", ["イッピン"], []),
    ],
    # Lesson 534[cite: 51]
    [
        ("骸", "むくろ", "body / corpse", ["ガイ"], ["むくろ"]),
        ("形骸", "けいがい", "ruins / wreck / mere shell / framework", ["ケイガイ"], []),
        ("麺", "めん", "noodles / wheat flour", ["メン", "ベン"], ["むぎこ"]),
        ("鈍感", "どんかん", "thickheaded / dull / insensitive / obtuse", ["ドンカン"], []),
        ("見苦しい", "みぐるしい", "unsightly / ugly / unseemly / disgraceful", [], ["みぐる.しい"]),
    ],
    # Lesson 535[cite: 51]
    [
        ("家族連れ", "かぞくづれ", "with one's family / family group", [], ["かぞくづれ"]),
        ("待ち遠しい", "まちどおしい", "looking forward to / waiting impatiently for", [], ["まちどお.しい"]),
        ("貪欲", "どんよく", "avarice / greed / covetousness", ["ドンヨク"], []),
        ("先駆け", "さきがけ", "pioneer / leader / taking the initiative", [], ["さきがけ"]),
        ("資金繰り", "しきんぐり", "financing / fund management / cash flow", ["シキングリ"], []),
    ],
    # Lesson 536[cite: 51]
    [
        ("萎む", "しぼむ", "to wither / fade (away) / shrivel / wilt", ["イ"], ["しぼ.む", "しお.れる"]),
        ("翻弄", "ほんろう", "toying with / trifling with / tossing about", ["ホンロウ"], []),
        ("転嫁", "てんか", "imputation / shifting (blame, responsibility)", ["テンカ"], []),
        ("速攻", "そっこう", "swift attack / fast break", ["ソッコウ"], []),
        ("地雷", "じらい", "land mine / taboo topic", ["ジライ"], []),
    ],
    # Lesson 537[cite: 51]
    [
        ("脱皮", "だっぴ", "ecdysis / shedding (of skin) / sloughing", ["ダッピ"], []),
        ("扇", "おうぎ", "folding fan", ["セン"], ["おうぎ"]),
        ("茨城", "いばらき", "Ibaraki", [], ["いばらき"]),
        ("枯渇", "こかつ", "drying up / running dry / exhaustion", ["コカツ"], []),
        ("寄席", "よせ", "vaudeville / rakugo variety theater", [], ["よせ"]),
    ],
    # Lesson 538[cite: 51]
    [
        ("優劣", "ゆうれつ", "superiority or inferiority / relative merits", ["ユウレツ"], []),
        ("老ける", "ふける", "to age / grow old", ["ロウ"], ["ふ.ける"]),
        ("奪取", "だっしゅ", "capture / seizure / recapture", ["ダッシュ"], []),
        ("寄贈", "きぞう", "donation / presentation / gift", ["キゾウ"], []),
        ("撲滅", "ぼくめつ", "eradication / extermination / destruction", ["ボクメツ"], []),
    ],
    # Lesson 539[cite: 51]
    [
        ("同い年", "おないどし", "the same age", [], ["おないどし"]),
        ("生い立ち", "おいたち", "early life / upbringing / personal history", [], ["おいたち"]),
        ("転覆", "てんぷく", "overturning / capsizing / overthrow", ["テンプク"], []),
        ("捗る", "はかどる", "to make progress / move right ahead (with work)", ["チョク"], ["はかど.る"]),
        ("栃木", "とちぎ", "Tochigi", [], ["とちぎ"]),
    ],
    # Lesson 540[cite: 50]
    [
        ("真心", "まごころ", "sincerity / devotion", [], ["まごころ"]),
        ("見え隠れ", "みえがくれ", "appearing and disappearing", [], ["みえがくれ"]),
        ("鍵盤", "けんばん", "keyboard (piano, organ, etc.)", ["ケンバン"], []),
        ("急かす", "せかす", "to hurry / urge on", [], ["せか.す"]),
        ("摂理", "せつり", "providence (of God) / laws of nature", ["セツリ"], []),
    ],
    # Lesson 541[cite: 50]
    [
        ("粉砕", "ふんさい", "pulverization / smashing / crushing", ["フンサイ"], []),
        ("厳か", "おごそか", "majestic / dignified / solemn / stately", ["ゲン"], ["おごそ.か"]),
        ("報い", "むくい", "reward / recompense / retribution", ["ホウ"], ["むく.い"]),
        ("給仕", "きゅうじ", "office boy (girl) / page / waiter / waitress", ["キュウジ"], []),
        ("老若男女", "ろうにゃくなんにょ", "men and women of all ages", ["ロウニャクナンニョ"], []),
    ],
    # Lesson 542[cite: 50]
    [
        ("親睦", "しんぼく", "friendship / intimacy / friendly relations", ["シンボク"], []),
        ("卑劣", "ひれつ", "mean / contemptible / cowardly / despicable", ["ヒレツ"], []),
        ("号泣", "ごうきゅう", "lamentation / wailing", ["ゴウキュウ"], []),
        ("生臭い", "なまぐさい", "smelling of fish or blood / fishy / bloody", [], ["なまぐさ.い"]),
        ("記念碑", "きねんひ", "monument / memorial", ["キネンヒ"], []),
    ],
    # Lesson 543[cite: 50]
    [
        ("冥福", "めいふく", "happiness in the next world", ["メイフク"], []),
        ("鍛冶", "かじ", "smithing / blacksmith", ["カジ"], []),
        ("怠慢", "たいまん", "negligence / carelessness / procrastination", ["タイマン"], []),
        ("羊毛", "ようもう", "wool", ["ヨウモウ"], []),
        ("公司", "こんす", "company / firm", ["コンス"], []),
    ],
    # Lesson 544[cite: 50]
    [
        ("荷造り", "にづくり", "packing / baling / crating", [], ["にづくり"]),
        ("煙る", "けむる", "to smoke / be smoky / look hazy", ["エン"], ["けむ.る"]),
        ("罵倒", "ばとう", "denunciation / abuse / reviling / vituperation", ["バトウ"], []),
        ("刷新", "さっしん", "reform / innovation / renovation / renewal", ["サッシン"], []),
        ("陳腐", "ちんぷ", "hackneyed / stale / trite / commonplace", ["チンプ"], []),
    ],
    # Lesson 545[cite: 50]
    [
        ("興味津々", "きょうみしんしん", "very interesting / of absorbing interest", ["キョウミシンシン"], []),
        ("島国", "しまぐに", "island country", ["トウコク"], ["しまぐに"]),
        ("謙遜", "けんそん", "humility / modesty", ["ケンソン"], []),
        ("最高峰", "さいこうほう", "highest peak / highest authority", ["サイコウホウ"], []),
        ("惨敗", "ざんぱい", "crushing defeat / ignominious defeat", ["ザンパイ"], []),
    ],
    # Lesson 546[cite: 50]
    [
        ("研磨", "けんま", "grinding / polishing / study / self-improvement", ["ケンマ"], []),
        ("愛媛", "えひめ", "Ehime", [], ["えひめ"]),
        ("警鐘", "けいしょう", "alarm bell / warning", ["ケイショウ"], []),
        ("白血病", "はっけつびょう", "leukemia", ["ハッケツビョウ"], []),
        ("滋賀", "しが", "Shiga", [], ["しが"]),
    ],
    # Lesson 547[cite: 50]
    [
        ("狙撃", "そげき", "shooting / sniping", ["ソゲキ"], []),
        ("繕う", "つくろう", "to mend / patch up / repair / fix / keep up appearances", ["ゼン"], ["つくろ.う"]),
        ("以て", "もって", "with / by / by means of / because / in view of", ["イ"], ["もっ.て"]),
        ("代わる代わる", "かわるがわる", "alternately / by turns / one after another", [], ["かわるがわる"]),
        ("物好き", "ものずき", "curiosity / whim / eccentricity", [], ["ものずき"]),
    ],
    # Lesson 548[cite: 50]
    [
        ("哀愁", "あいしゅう", "pathos / sorrow / grief / sadness / melancholy", ["アイシュウ"], []),
        ("海路", "かいろ", "sea route / by sea", ["カイロ"], []),
        ("論評", "ろんぴょう", "comment / review / criticism", ["ロンピョウ"], []),
        ("渡り鳥", "わたりどり", "migratory bird / bird of passage", [], ["わたりどり"]),
        ("蛇足", "だそく", "redundancy / superfluity / needless addition", ["ダソク"], []),
    ],
    # Lesson 549[cite: 50]
    [
        ("独禁法", "どっきんほう", "Antimonopoly Law / Antitrust Law", ["ドッキンホウ"], []),
        ("句読点", "くとうてん", "punctuation marks", ["クトウテン"], []),
        ("脱臼", "だっきゅう", "dislocation (of a joint)", ["ダッキュウ"], []),
        ("弦楽", "げんがく", "string music", ["ゲンガク"], []),
        ("骨太", "ほねぶと", "big-boned / sturdy / bold / solid (policy)", [], ["ほねぶと"]),
    ],
    # Lesson 550[cite: 50]
    [
        ("旅客機", "りょかくき", "passenger aircraft", ["リョカクキ"], []),
        ("斜", "しゃ", "diagonal / slanting / oblique", ["シャ"], ["なな.め"]),
        ("戯言", "たわごと", "nonsense / silly talk / gibberish", ["ギゲン"], ["たわごと"]),
        ("大相撲", "おおずもう", "professional sumo wrestling", ["オオズモウ"], []),
        ("泡盛", "あわもり", "awamori (Okinawan distilled liquor)", [], ["あわもり"]),
    ],
    # Lesson 551[cite: 52]
    [
        ("汚らわしい", "けがらわしい", "filthy / dirty / impure / disgusting", ["オ"], ["けが.らわしい"]),
        ("真っ二つ", "まっぷたつ", "in two equal parts / right in half", [], ["まっぷたつ"]),
        ("弔い", "とむらい", "funeral / mourning / condolence", ["チョウ"], ["とむら.い"]),
        ("芽生え", "めばえ", "bud / sprout / germ / beginning", ["ガ"], ["めば.え"]),
        ("萎びる", "しなびる", "to wilt / wither / shrivel", ["イ"], ["しな.びる"]),
    ],
    # Lesson 552[cite: 52]
    [
        ("御社", "おんしゃ", "your company (honorific)", ["オンシャ"], []),
        ("海賊版", "かいぞくばん", "pirated edition / bootleg", ["カイゾクバン"], []),
        ("月賦", "げっぷ", "monthly installment", ["ゲップ"], []),
        ("典範", "てんぱん", "authoritative guide / standard / model / law", ["テンパン"], []),
        ("刺", "とげ", "thorn / splinter / spine / biting words", ["シ"], ["とげ"]),
    ],
    # Lesson 553[cite: 52]
    [
        ("新譜", "しんぷ", "new record / new release (music)", ["シンプ"], []),
        ("接ぐ", "つぐ", "to join / piece together / set (bones) / graft", ["セツ"], ["つ.ぐ"]),
        ("面子", "めんつ", "face / honor / prestige", ["メンツ"], []),
        ("言伝", "ことづて", "verbal message / word", [], ["ことづて"]),
        ("伎", "ぎ", "deed / skill", ["ギ", "キ"], ["わざ"]),
    ],
    # Lesson 554[cite: 52]
    [
        ("詰将棋", "つめしょうぎ", "shogi end-game puzzle / checkmate problem", ["ツメショウギ"], []),
        ("垣間見", "かいまみ", "glimpse / peep", [], ["かいまみ"]),
        ("お出でになる", "おいでになる", "to be / come / go (honorific)", [], ["おいでになる"]),
        ("傲る", "おごる", "to be proud / be haughty / be arrogant", ["ゴウ"], ["おご.る"]),
    ],
    # Lesson 555[cite: 52]
    [
        ("お目出度う", "おめでとう", "congratulations! / best wishes!", [], ["おめでとう"]),
        ("省みる", "かえりみる", "to look back on (the past) / reflect", ["セイ", "ショウ"], ["かえり.みる"]),
        ("畏まりました", "かしこまりました", "certainly! / very well, sir/madam", [], ["かしこまりました"]),
        ("箇箇", "ここ", "individually / separately / one by one", ["ココ"], []),
        ("その外", "そのほか", "besides / in addition / otherwise / the rest", [], ["そのほか"]),
    ],
    # Lesson 556[cite: 52]
    [
        ("捻子", "ねじ", "screw", ["ネン"], ["ねじ"]),
        ("打付ける", "ぶつける", "to knock / run into / nail on / strike hard", [], ["ぶつ.ける"]),
        ("真に", "まことに", "indeed / really / truly / actually", ["シン"], ["まこと.に"]),
        ("愛でたい", "めでたい", "happy / auspicious / joyous / congratulatory", [], ["めでた.い"]),
    ],
    # Lesson 557[cite: 52]
    [
        ("好い", "よい", "good / fine / nice / pleasant", ["コウ"], ["よ.い"]),
        ("依って", "よって", "therefore / consequently / accordingly", ["イ"], ["よ.って"]),
        ("煎る", "いる", "to parch / roast / fry / boil down", ["セン"], ["い.る"]),
    ],
    # Lesson 558[cite: 52]
    [
        ("卸す", "おろす", "to sell wholesale / grated (vegetables)", ["シャ"], ["おろ.す"]),
        ("街角", "まちかど", "street corner", [], ["まちかど"]),
        ("聴く", "きく", "to listen (e.g. to music) / hear", ["チョウ"], ["き.く"]),
        ("応える", "こたえる", "to respond / answer / meet (expectations)", ["オウ"], ["こた.える"]),
    ],
    # Lesson 559[cite: 52]
    [
        ("闘う", "たたかう", "to make war (on) / battle / struggle / fight", ["トウ"], ["たたか.う"]),
        ("創る", "つくる", "to create / make / originate", ["ソウ", "ショウ"], ["つく.る"]),
        ("哀しい", "かなしい", "sad / sorrowful", ["アイ"], ["かな.しい"]),
        ("苗字", "みょうじ", "surname / family name", ["ミョウジ"], []),
    ],
]


def get_strokes_for_char(ch: str) -> list[str]:
    hex_code = f"{ord(ch):05x}"
    svg_path = os.path.join(KANJIVG_DIR, f"{hex_code}.svg")
    if not os.path.exists(svg_path):
        print(f"WARNING: Missing SVG for '{ch}' ({hex_code}.svg)")
        return []
    tree = ET.parse(svg_path)
    root = tree.getroot()
    strokes = []
    for elem in root.iter():
        if elem.tag.endswith("path"):
            d = elem.attrib.get("d")
            if d:
                strokes.append(d.strip())
    return strokes


def main():
    if not os.path.exists(PART4_JSON_PATH):
        raise FileNotFoundError(f"Run 'python generate_n1_part4.py' first to create {PART4_JSON_PATH}.")

    with open(PART4_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N1_PART5_DATA):
        lesson_num = 500 + l_idx
        lesson_items = []

        for word, kana, meaning, onyomi, kunyomi in chunk:
            characters_data = []
            for ch in word:
                characters_data.append({
                    "char": ch,
                    "strokes": get_strokes_for_char(ch),
                })

            lesson_items.append({
                "id": f"n1-{item_counter}",
                "level": "N1",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n1-lesson-{lesson_num}",
            "level": "N1",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    os.makedirs(os.path.dirname(OUTPUT_TS_PATH), exist_ok=True)
    ts_content = (
        "import type { KanjiLesson } from '../types/kanji';\n\n"
        f"export const N1_LESSONS: KanjiLesson[] = {json.dumps(lessons, ensure_ascii=False, indent=2)};\n"
    )

    with open(OUTPUT_TS_PATH, "w", encoding="utf-8") as f:
        f.write(ts_content)

    for temp_file in [PART1_JSON_PATH, PART2_JSON_PATH, PART3_JSON_PATH, PART4_JSON_PATH]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"Done! Compiled all {len(lessons)} N1 lessons ({item_counter - 1} items) into {OUTPUT_TS_PATH}.")


if __name__ == "__main__":
    main()