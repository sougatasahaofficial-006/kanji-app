import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n2_part1.json"
OUTPUT_TS_PATH = os.path.join("src", "data", "n2.ts")

N2_PART2_DATA = [
    # Lesson 116[cite: 40]
    [
        ("爆", "ばく", "bomb / burst / explode", ["バク"], ["は.ぜる"]),
        ("爆発", "ばくはつ", "explosion / detonation", ["バクハツ"], []),
        ("捜す", "さがす", "to search for (lost item/person)", ["ソウ"], ["さが.す"]),
        ("述", "じゅつ", "mention / state / speak", ["ジュツ"], ["の.べる"]),
        ("含有", "がんゆう", "containing / content", ["ガンユウ"], []),
    ],
    # Lesson 117[cite: 40]
    [
        ("石油", "せきゆ", "oil / petroleum", ["セキユ"], []),
        ("叫ぶ", "さけぶ", "to shout / cry out", ["キョウ"], ["さけ.ぶ"]),
        ("伸ばす", "のばす", "to lengthen / stretch / extend", ["シン"], ["の.ばす", "の.びる"]),
        ("伸びる", "のびる", "to stretch / grow / extend", ["シン"], ["の.びる"]),
        ("所以", "ゆえん", "reason / grounds", [], ["ゆえん"]),
    ],
    # Lesson 118[cite: 40]
    [
        ("承る", "うけたまわる", "to hear / be told / receive (humble)", ["ショウ"], ["うけたまわ.る"]),
        ("承認", "しょうにん", "approval / recognition", ["ショウニン"], []),
        ("承知", "しょうち", "consent / acceptance / knowledge", ["ショウチ"], []),
        ("承知する", "しょうちする", "to agree / consent / understand", ["ショウチ"], []),
        ("清水", "しみず", "spring water / Shimizu", [], ["しみず"]),
    ],
    # Lesson 119[cite: 40]
    [
        ("雲", "くも", "cloud", ["ウン"], ["くも"]),
        ("練る", "ねる", "to knead / polish / work out", ["レン"], ["ね.る"]),
        ("練習", "れんしゅう", "practice / training", ["レンシュウ"], []),
        ("紹", "しょう", "introduce / inherit", ["ショウ"], []),
        ("短冊", "たんざく", "strip of paper (for poems/wishes)", ["タンザク"], []),
    ],
    # Lesson 120[cite: 40]
    [
        ("紹介", "しょうかい", "introduction", ["ショウカイ"], []),
        ("包む", "つつむ", "to wrap up / pack", ["ホウ"], ["つつ.む"]),
        ("小包", "こづつみ", "parcel / package", [], ["こづつみ"]),
        ("包帯", "ほうたい", "bandage / dressing", ["ホウタイ"], []),
        ("月日", "つきひ", "time / years / days", [], ["つきひ"]),
    ],
    # Lesson 121[cite: 40]
    [
        ("庁", "ちょう", "government office / agency", ["チョウ"], []),
        ("県庁", "けんちょう", "prefectural office", ["ケンチョウ"], []),
        ("官庁", "かんちょう", "government office / authorities", ["カンチョウ"], []),
        ("測る", "はかる", "to measure / survey", ["ソク"], ["はか.る"]),
        ("空っぽ", "からっぽ", "empty / vacant / hollow", [], ["からっぽ"]),
    ],
    # Lesson 122[cite: 40]
    [
        ("測定", "そくてい", "measurement", ["ソクテイ"], []),
        ("測量", "そくりょう", "surveying", ["ソクリョウ"], []),
        ("観測", "かんそく", "observation", ["カンソク"], []),
        ("予測", "よそく", "prediction / estimation", ["ヨソク"], []),
        ("綿密", "めんみつ", "minute / detailed / meticulous", ["メンミツ"], []),
    ],
    # Lesson 123[cite: 41]
    [
        ("占う", "うらなう", "to forecast / tell fortunes", ["セン"], ["し.める", "うらな.う"]),
        ("占める", "しめる", "to occupy / hold / account for", ["セン"], ["し.める"]),
        ("混む", "こむ", "to be crowded", ["コン"], ["こ.む", "ま.ざる"]),
        ("混ぜる", "まぜる", "to mix / stir / blend", ["コン"], ["ま.ぜる"]),
        ("二階建て", "にかいだて", "two-storied building", [], ["にかいだて"]),
    ],
    # Lesson 124[cite: 41]
    [
        ("混雑", "こんざつ", "congestion / crowding", ["コンザツ"], []),
        ("混乱", "こんらん", "disorder / chaos / confusion", ["コンラン"], []),
        ("倍", "ばい", "double / twice / times", ["バイ"], []),
        ("乳", "ちち", "milk / breast", ["ニュウ"], ["ちち", "ち"]),
        ("軽やか", "かろやか", "light / nimble / effortless", ["ケイ"], ["かろ.やか"]),
    ],
    # Lesson 125[cite: 41]
    [
        ("乳児", "にゅうじ", "infant / baby", ["ニュウジ"], []),
        ("牛乳", "ぎゅうにゅう", "cow's milk", ["ギュウニュウ"], []),
        ("荒い", "あらい", "rough / wild / rude", ["コウ"], ["あら.い", "あ.れる"]),
        ("詰める", "つめる", "to pack / stuff / shorten", ["キツ"], ["つ.める", "つ.まる"]),
        ("昔話", "むかしばなし", "old tale / folklore", [], ["むかしばなし"]),
    ],
    # Lesson 126[cite: 41]
    [
        ("栄える", "さかえる", "to prosper / flourish", ["エイ"], ["さか.える", "は.える"]),
        ("律", "りつ", "rhythm / law / regulation", ["リツ", "リチ"], []),
        ("則", "そく", "rule / law / follow", ["ソク"], ["のっと.る"]),
        ("規則", "きそく", "rule / regulation", ["キソク"], []),
        ("待合室", "まちあいしつ", "waiting room", [], ["まちあいしつ"]),
    ],
    # Lesson 127[cite: 41]
    [
        ("禁じる", "きんじる", "to forbid / ban / prohibit", ["キン"], ["きん.じる"]),
        ("禁煙", "きんえん", "no smoking", ["キンエン"], []),
        ("立ち入り禁止", "たちいりきんし", "keep out / off limits", [], ["たちいりきんし"]),
        ("順", "じゅん", "order / turn", ["ジュン"], []),
        ("酒場", "さかば", "bar / tavern / pub", [], ["さかば"]),
    ],
    # Lesson 128[cite: 41]
    [
        ("順調", "じゅんちょう", "favorable / doing well", ["ジュンチョウ"], []),
        ("枚", "まい", "counter for flat objects", ["マイ", "バイ"], []),
        ("一枚", "いちまい", "one sheet/flat object", ["イチマイ"], []),
        ("五枚", "ごまい", "five sheets/flat objects", ["ゴマイ"], []),
        ("後々", "のちのち", "in the future / later on", [], ["のちのち"]),
    ],
    # Lesson 129[cite: 41]
    [
        ("厚い", "あつい", "thick / kind / cordial", ["コウ"], ["あつ.い"]),
        ("輸", "ゆ", "transport / send", ["ユ", "シュ"], []),
        ("輸出", "ゆしゅつ", "export", ["ユシュツ"], []),
        ("輸入", "ゆにゅう", "import", ["ユニュウ"], []),
        ("厚生", "こうせい", "public welfare", ["コウセイ"], []),
    ],
    # Lesson 130[cite: 41]
    [
        ("濃い", "こい", "thick / dense / strong / dark", ["ノウ"], ["こ.い"]),
        ("簡", "かん", "simplicity / brevity", ["カン"], []),
        ("簡単", "かんたん", "simple / easy", ["カンタン"], []),
        ("孫", "まご", "grandchild", ["ソン"], ["まご"]),
        ("濃度", "のうど", "concentration / density", ["ノウド"], []),
    ],
    # Lesson 131[cite: 41]
    [
        ("丈", "たけ", "height / stature / length", ["ジョウ"], ["たけ"]),
        ("丈夫", "じょうぶ", "healthy / strong / durable", ["ジョウブ"], []),
        ("大丈夫", "だいじょうぶ", "all right / safe / okay", ["ダイジョウブ"], []),
        ("子孫", "しそん", "descendant / offspring", ["シソン"], []),
        ("覚書", "おぼえがき", "memorandum / note", [], ["おぼえがき"]),
    ],
    # Lesson 132[cite: 41]
    [
        ("黄", "き", "yellow", ["コウ", "オウ"], ["き", "こ-"]),
        ("黄色い", "きいろい", "yellow", ["オウショク"], ["きいろ.い"]),
        ("届く", "とどく", "to reach / arrive", ["トドケ"], ["とど.く", "とど.ける"]),
        ("届ける", "とどける", "to deliver / report / notify", [], ["とど.ける"]),
        ("届出", "とどけで", "report / notification", [], ["とどけで"]),
    ],
    # Lesson 133[cite: 41]
    [
        ("絡む", "からむ", "to entangle / get involved", ["ラク"], ["から.む", "から.まる"]),
        ("連絡", "れんらく", "contact / communication", ["レンラク"], []),
        ("採る", "とる", "to adopt / pick / gather", ["サイ"], ["と.る"]),
        ("採用", "さいよう", "adoption / employment / hiring", ["サイヨウ"], []),
        ("始終", "しじゅう", "continuously / always", ["シジュウ"], []),
    ],
    # Lesson 134[cite: 41]
    [
        ("傾く", "かたむく", "to incline / lean / tilt", ["ケイ"], ["かたむ.く", "かたむ.ける"]),
        ("朗らか", "ほがらか", "bright / cheerful / melodious", ["ロウ"], ["ほが.らか"]),
        ("傾向", "けいこう", "tendency / trend / inclination", ["ケイコウ"], []),
        ("鼻", "はな", "nose", ["ビ"], ["はな"]),
        ("積雪", "せきせつ", "fallen snow / snow cover", ["セキセツ"], []),
    ],
    # Lesson 135[cite: 41]
    [
        ("鼻水", "はなみず", "runny nose / nasal mucus", [], ["はなみず"]),
        ("鼻が高い", "はながたかい", "proud / boastful", [], ["はながたか.い"]),
        ("宝", "たから", "treasure", ["ホウ"], ["たから"]),
        ("宝石", "ほうせき", "gem / jewel", ["ホウセキ"], []),
        ("日本橋", "にほんばし", "Nihonbashi", [], ["にほんばし"]),
    ],
    # Lesson 136[cite: 41]
    [
        ("患う", "わずらう", "to fall ill / suffer from", ["カン"], ["わずら.う"]),
        ("患者", "かんじゃ", "patient", ["カンジャ"], []),
        ("入院患者", "にゅういんかんじゃ", "inpatient", ["ニュウインカンジャ"], []),
        ("延ばす", "のばす", "to postpone / extend / prolong", ["エン"], ["の.ばす", "の.びる"]),
        ("絶叫", "ぜっきょう", "scream / shriek / exclamation", ["ゼッキョウ"], []),
    ],
    # Lesson 137[cite: 41]
    [
        ("延びる", "のびる", "to be prolonged / extended", ["エン"], ["の.びる"]),
        ("延期", "えんき", "postponement / deferment", ["エンキ"], []),
        ("律", "りつ", "law / rhythm / regulation", ["リツ", "リチ"], []),
        ("法律", "ほうりつ", "law", ["ホウリツ"], []),
        ("置き去り", "おきざり", "desertion / leaving behind", [], ["おきざり"]),
    ],
    # Lesson 138[cite: 41]
    [
        ("希", "まれ", "rare / phenomenal", ["キ", "ケ"], ["まれ"]),
        ("希望", "きぼう", "hope / wish / aspiration", ["キボウ"], []),
        ("甘い", "あまい", "sweet / indulgent / naive", ["カン"], ["あま.い", "あま.える"]),
        ("甘やかす", "あまやかす", "to pamper / spoil", ["カン"], ["あま.やかす"]),
        ("希薄", "きはく", "thin / dilute / sparse", ["キハク"], []),
    ],
    # Lesson 139[cite: 41]
    [
        ("湾", "わん", "gulf / bay / inlet", ["ワン"], []),
        ("台湾", "たいわん", "Taiwan", ["タイワン"], []),
        ("沈む", "しずむ", "to sink / feel depressed", ["チン"], ["しず.む", "しず.める"]),
        ("販", "はん", "marketing / sell / trade", ["ハン"], []),
        ("お上", "おかみ", "the government / authorities", [], ["おかみ"]),
    ],
    # Lesson 140[cite: 41]
    [
        ("販売", "はんばい", "sales / selling", ["ハンバイ"], []),
        ("自動販売機", "じどうはんばいき", "vending machine", ["ジドウハンバイキ"], []),
        ("欧", "おう", "Europe", ["オウ"], []),
        ("欧米", "おうべい", "Europe and America / the West", ["オウベイ"], []),
        ("流布", "るふ", "circulation / dissemination", ["ルフ"], []),
    ],
    # Lesson 141[cite: 41]
    [
        ("砂", "すな", "sand", ["サ", "シャ"], ["すな"]),
        ("尊い", "とうとい", "precious / noble / sacred", ["ソン"], ["たっと.い", "とうと.い"]),
        ("尊重", "そんちょう", "respect / esteem / regard", ["ソンチョウ"], []),
        ("紅", "べに", "crimson / deep red / lipstick", ["コウ", "ク"], ["べに", "くれない"]),
        ("鉄板", "てっぱん", "iron plate / hot plate", ["テッパン"], []),
    ],
    # Lesson 142[cite: 41]
    [
        ("口紅", "くちべに", "lipstick", [], ["くちべに"]),
        ("紅茶", "こうちゃ", "black tea", ["コウチャ"], []),
        ("紅葉", "こうよう", "autumn leaves / fall foliage", ["コウヨウ"], ["もみじ"]),
        ("複", "ふく", "duplicate / double / compound", ["フク"], []),
        ("木工", "もっこう", "woodworking / carpenter", ["モッコウ"], []),
    ],
    # Lesson 143[cite: 42]
    [
        ("複雑", "ふくざつ", "complicated / complex", ["フクザツ"], []),
        ("泊まる", "とまる", "to stay at (e.g. hotel)", ["ハク"], ["と.まる", "と.める"]),
        ("泊まり", "とまり", "overnight stay / lodging", ["ハク"], ["と.まり"]),
        ("宿泊", "しゅくはく", "lodging / accommodation", ["シュクハク"], []),
        ("一泊", "いっぱく", "one night's stay", ["イッパク"], []),
    ],
    # Lesson 144[cite: 42]
    [
        ("荷", "に", "load / baggage / cargo", ["カ"], ["に"]),
        ("荷物", "にもつ", "luggage / baggage", ["ニモツ"], []),
        ("枝", "えだ", "branch / bough / twig", ["シ"], ["えだ"]),
        ("依", "い", "reliant / depend on", ["イ", "エ"], []),
        ("負荷", "ふか", "burden / load", ["フカ"], []),
    ],
    # Lesson 145[cite: 42]
    [
        ("依頼", "いらい", "request / commission / dependence", ["イライ"], []),
        ("幼い", "おさない", "very young / childish", ["ヨウ"], ["おさな.い"]),
        ("幼なじみ", "おさななじみ", "childhood friend", [], ["おさななじみ"]),
        ("幼児", "ようじ", "toddler / young child", ["ヨウジ"], []),
        ("見栄え", "みばえ", "appearance / look", [], ["みばえ"]),
    ],
    # Lesson 146[cite: 42]
    [
        ("斬る", "きる", "to kill with a blade / slash", ["ザン"], ["き.る"]),
        ("勇ましい", "いさましい", "brave / valiant / gallant", ["ユウ"], ["いさ.ましい"]),
        ("勇気", "ゆうき", "courage / bravery", ["ユウキ"], []),
        ("昇る", "のぼる", "to ascend / rise", ["ショウ"], ["のぼ.る"]),
        ("斬新", "ざんしん", "novel / original / innovative", ["ザンシン"], []),
    ],
    # Lesson 147[cite: 42]
    [
        ("寿", "ことぶき", "longevity / congratulations", ["ジュ", "ス"], ["ことぶき"]),
        ("菜", "な", "vegetable / greens", ["サイ"], ["な"]),
        ("野菜", "やさい", "vegetable", ["ヤサイ"], []),
        ("季", "き", "seasons", ["キ"], []),
        ("寿命", "じゅみょう", "life span", ["ジュミョウ"], []),
    ],
    # Lesson 148[cite: 42]
    [
        ("四季", "しき", "the four seasons", ["シキ"], []),
        ("液", "えき", "liquid / fluid", ["エキ"], []),
        ("血液", "けつえき", "blood", ["ケツエキ"], []),
        ("血液型", "けつえきがた", "blood type", ["ケツエキガタ"], []),
        ("続行", "ぞっこう", "continuation / resuming", ["ゾッコウ"], []),
    ],
    # Lesson 149[cite: 42]
    [
        ("券", "けん", "ticket / coupon / certificate", ["ケン"], []),
        ("割引券", "わりびきけん", "discount coupon", ["ワリビキケン"], []),
        ("定期券", "ていきけん", "commuter pass", ["テイキケン"], []),
        ("祭", "まつり", "festival / feast", ["サイ"], ["まつ.る", "まつ.り"]),
        ("兵庫", "ひょうご", "Hyogo Prefecture", ["ヒョウゴ"], []),
    ],
    # Lesson 150[cite: 42]
    [
        ("お祭り", "おまつり", "festival", ["サイ"], ["まつ.り"]),
        ("祭日", "さいじつ", "national holiday / festival day", ["サイジツ"], []),
        ("袋", "ふくろ", "bag / sack / pouch", ["タイ", "ダイ"], ["ふくろ"]),
        ("レジ袋", "レジぶくろ", "plastic shopping bag", [], ["レジぶくろ"]),
        ("小切手", "こぎって", "check / cheque", [], ["こぎって"]),
    ],
    # Lesson 151[cite: 43]
    [
        ("手袋", "てぶくろ", "glove / mitten", [], ["てぶくろ"]),
        ("燃える", "もえる", "to burn / blaze", ["ネン"], ["も.える", "も.やす"]),
        ("毒", "どく", "poison / venom / harm", ["ドク"], []),
        ("気の毒", "きのどく", "pitiful / unfortunate / sorry", [], ["きのどく"]),
        ("谷川", "たにがわ", "mountain stream", [], ["たにがわ"]),
    ],
    # Lesson 152[cite: 43]
    [
        ("札", "ふだ", "tag / label / bill / card", ["サツ"], ["ふだ"]),
        ("名札", "なふだ", "name tag / nameplate", [], ["なふだ"]),
        ("改札", "かいさつ", "ticket gate / ticket examination", ["カイサツ"], []),
        ("改札口", "かいさつぐち", "ticket gate / wicket", ["カイサツグチ"], []),
        ("沖合", "おきあい", "offshore / out at sea", [], ["おきあい"]),
    ],
    # Lesson 153[cite: 43]
    [
        ("自動改札", "じどうかいさつ", "automatic ticket gate", ["ジドウカイサツ"], []),
        ("狙い", "ねらい", "aim / objective / target", ["ソ"], ["ねら.い"]),
        ("狙う", "ねらう", "to aim at", ["ソ"], ["ねら.う"]),
        ("綿", "わた", "cotton / padding", ["メン"], ["わた"]),
        ("自分勝手", "じぶんかって", "selfish / egoistic", ["ジブンカッテ"], []),
    ],
    # Lesson 154[cite: 43]
    [
        ("卒", "そつ", "graduate / soldier / finish", ["ソツ"], []),
        ("卒業", "そつぎょう", "graduation", ["ソツギョウ"], []),
        ("卒業式", "そつぎょうしき", "graduation ceremony", ["ソツギョウシキ"], []),
        ("油車", "ゆしゃ", "oil tank car", ["ユシャ"], []),
        ("校舎", "こうしゃ", "school building", ["コウシャ"], []),
    ],
    # Lesson 155[cite: 43]
    [
        ("副", "ふく", "vice- / assistant / duplicate", ["フク"], []),
        ("敬う", "うやまう", "to respect / revere / honor", ["ケイ"], ["うやま.う"]),
        ("尊敬", "そんけい", "respect / esteem", ["ソンケイ"], []),
        ("針", "はり", "needle / pin / hand (clock)", ["シン"], ["はり"]),
        ("方針", "ほうしん", "policy / course / plan", ["ホウシン"], []),
    ],
    # Lesson 156[cite: 43]
    [
        ("拝む", "おがむ", "to worship / pray / bow", ["ハイ"], ["おが.む"]),
        ("浴びる", "あびる", "to bathe / bask / be showered with", ["ヨク"], ["あ.びる", "あ.びせる"]),
        ("悩む", "なやむ", "to be worried / troubled", ["ノウ"], ["なや.む", "なや.ます"]),
        ("悩み", "なやみ", "trouble / worry / distress", ["ノウ"], ["なや.み"]),
        ("参拝", "さんぱい", "visit to a shrine/temple", ["サンパイ"], []),
    ],
    # Lesson 157[cite: 43]
    [
        ("汚い", "きたない", "dirty / filthy / unfair", ["オ"], ["きたな.い", "よご.れる"]),
        ("汚れ", "よごれ", "dirt / stain / filth", ["オ"], ["よご.れ"]),
        ("汚す", "よごす", "to pollute / dirty / stain", ["オ"], ["よご.す", "けが.す"]),
        ("汚れる", "よごれる", "to get dirty / become stained", ["オ"], ["よご.れる"]),
        ("苦悩", "くのう", "agony / anguish / suffering", ["クノウ"], []),
    ],
    # Lesson 158[cite: 43]
    [
        ("灯", "ひ", "light / lamp", ["トウ"], ["ひ", "ほ-", "ともしび"]),
        ("灯台", "とうだい", "lighthouse", ["トウダイ"], []),
        ("電灯", "でんとう", "electric light", ["デントウ"], []),
        ("灯油", "とうゆ", "kerosene / lamp oil", ["トウユ"], []),
        ("浴衣", "ゆかた", "yukata (summer cotton kimono)", [], ["ゆかた"]),
    ],
    # Lesson 159[cite: 43]
    [
        ("坊や", "ぼうや", "boy / little boy", ["ボウ", "ボッ"], []),
        ("坊さん", "ぼうさん", "Buddhist priest / monk", ["ボウ"], []),
        ("坊ちゃん", "ぼっちゃん", "young master / son (polite)", ["ボッ"], []),
        ("坊っちゃん", "ぼっちゃん", "young master / naive rich boy", ["ボッ"], []),
        ("坊主", "ぼうず", "Buddhist priest / shaven head", ["ボウズ"], []),
    ],
    # Lesson 160[cite: 43]
    [
        ("寝坊", "ねぼう", "sleeping in late / oversleeping", ["ネボウ"], []),
        ("お尻", "おしり", "buttocks / bottom", [], ["おしり"]),
        ("涙", "なみだ", "tear / tears", ["ルイ"], ["なみだ"]),
        ("バス停", "バスてい", "bus stop", ["テイ"], []),
        ("精進", "しょうじん", "devotion / vegetarian diet", ["ショウジン"], []),
    ],
    # Lesson 161[cite: 43]
    [
        ("停車", "ていしゃ", "stopping (of a train/car)", ["テイシャ"], []),
        ("停電", "ていでん", "power outage / blackout", ["テイデン"], []),
        ("停留所", "ていりゅうじょ", "bus/tram stop", ["テイリュウジョ"], []),
        ("各駅停車", "かくえきていしゃ", "local train (stops at every station)", ["カクエキテイシャ"], []),
        ("複製", "ふくせい", "reproduction / duplication", ["フクセイ"], []),
    ],
    # Lesson 162[cite: 43]
    [
        ("了", "りょう", "complete / finish", ["リョウ"], []),
        ("完了", "かんりょう", "completion / conclusion", ["カンリョウ"], []),
        ("汗", "あせ", "sweat / perspiration", ["カン"], ["あせ"]),
        ("蛇", "へび", "snake / serpent", ["ジャ", "ダ"], ["へび"]),
        ("将来", "しょうらい", "future", ["ショウライ"], []),
    ],
    # Lesson 163[cite: 43]
    [
        ("絶滅", "ぜつめつ", "extinction", ["ゼツメツ"], []),
        ("郵便局", "ゆうびんきょく", "post office", ["ユウビンキョク"], []),
        ("幅", "はば", "width / breadth", ["フク"], ["はば"]),
        ("量", "りょう", "quantity / amount", ["リョウ"], []),
        ("増幅", "ぞうふく", "amplification", ["ゾウフク"], []),
    ],
    # Lesson 164[cite: 43]
    [
        ("児童", "じどう", "children / juvenile", ["ジドウ"], []),
        ("埋める", "うめる", "to bury / fill up", ["マイ"], ["う.める", "う.まる"]),
        ("闇", "やみ", "darkness / the dark", ["アン"], ["やみ"]),
        ("棒", "ぼう", "pole / rod / stick", ["ボウ"], []),
        ("天下り", "あまくだり", "descent from heaven / golden parachute", [], ["あまくだり"]),
    ],
    # Lesson 165[cite: 43]
    [
        ("貨", "か", "freight / goods / property", ["カ"], []),
        ("貨物", "かもつ", "cargo / freight", ["カモツ"], []),
        ("硬貨", "こうか", "coin / hard currency", ["コウカ"], []),
        ("泉", "いずみ", "spring / fountain", ["セン"], ["いずみ"]),
        ("百貨店", "ひゃっかてん", "department store", ["ヒャッカテン"], []),
    ],
    # Lesson 166[cite: 43]
    [
        ("肌着", "はだぎ", "underwear / undershirt", [], ["はだぎ"]),
        ("臓", "ぞう", "entrails / viscera / internal organs", ["ゾウ"], []),
        ("心臓", "しんぞう", "heart (organ)", ["シンゾウ"], []),
        ("塩", "しお", "salt", ["エン"], ["しお"]),
        ("塩分", "えんぶん", "salt content / salinity", ["エンブン"], []),
    ],
    # Lesson 167[cite: 43]
    [
        ("塩辛い", "しおからい", "salty", [], ["しおから.い"]),
        ("均す", "ならす", "to level / smooth / average", ["キン"], ["なら.す"]),
        ("平均", "へいきん", "average / mean", ["ヘイキン"], []),
        ("平均点", "へいきんてん", "average score / mean mark", ["ヘイキンテン"], []),
        ("生る", "なる", "to bear fruit", ["セイ"], ["な.る"]),
    ],
    # Lesson 168[cite: 43]
    [
        ("湖", "みずうみ", "lake", ["コ"], ["みずうみ"]),
        ("摘", "てき", "pick / pluck / summarize", ["テキ"], ["つ.む"]),
        ("嫁", "よめ", "bride / wife", ["カ"], ["よめ", "とつ.ぐ"]),
        ("双", "そう", "pair / set / both", ["ソウ"], ["ふた"]),
        ("時価", "じか", "current market price", ["ジカ"], []),
    ],
    # Lesson 169[cite: 43]
    [
        ("双子", "ふたご", "twins", [], ["ふたご"]),
        ("軒", "けん", "house counter / eaves", ["ケン"], ["のき"]),
        ("境", "きょう", "border / region / state", ["キョウ", "ケイ"], ["さかい"]),
        ("成績", "せいせき", "results / grades / record", ["セイセキ"], []),
        ("一軒", "いっけん", "one house/building", ["イッケン"], []),
    ],
    # Lesson 170[cite: 43]
    [
        ("姓", "せい", "surname / family name", ["セイ", "ショウ"], []),
        ("踊る", "おどる", "to dance", ["ヨウ"], ["おど.る", "おど.り"]),
        ("籍", "せき", "enroll / domicile / register", ["セキ"], []),
        ("国籍", "こくせき", "nationality / citizenship", ["コクセキ"], []),
        ("百姓", "ひゃくしょう", "farmer / peasant", ["ヒャクショウ"], []),
    ],
    # Lesson 171[cite: 43]
    [
        ("書籍", "しょせき", "books / publications", ["ショセキ"], []),
        ("珍しい", "めずらしい", "unusual / rare / curious", ["チン"], ["めずら.しい"]),
        ("肌", "はだ", "skin", ["キ"], ["はだ"]),
        ("夫婦", "ふうふ", "married couple", ["フウフ"], []),
        ("床の間", "とこのま", "alcove (in Japanese room)", [], ["とこのま"]),
    ],
    # Lesson 172[cite: 43]
    [
        ("預ける", "あずける", "to deposit / leave in care of", ["ヨ"], ["あず.ける", "あず.かる"]),
        ("預かる", "あずかる", "to keep / take custody of", ["ヨ"], ["あず.かる"]),
        ("預金", "よきん", "deposit / bank account", ["ヨキン"], []),
        ("著", "ちょ", "renowned / publish / write", ["チョ"], ["あらわ.す"]),
        ("人妻", "ひとづま", "married woman", [], ["ひとづま"]),
    ],
    # Lesson 173[cite: 43]
    [
        ("著名", "ちょめい", "famous / noted / prominent", ["チョメイ"], []),
        ("原作者", "げんさくしゃ", "original author", ["ゲンサクシャ"], []),
        ("漁", "りょう", "fishing / fishery", ["ギョ", "リョウ"], []),
        ("漁業", "ぎょぎょう", "fishing industry", ["ギョギョウ"], []),
        ("絵文字", "えもじ", "emoji / pictograph", [], ["えもじ"]),
    ],
    # Lesson 174[cite: 43]
    [
        ("漁師", "りょうし", "fisherman", ["リョウシ"], []),
        ("緑", "みどり", "green / greenery", ["リョク", "ロク"], ["みどり"]),
        ("香", "かおり", "incense / fragrance / perfume", ["コウ", "キョウ"], ["か", "かお.り"]),
        ("咲く", "さく", "to bloom / blossom", ["ショウ"], ["さ.く"]),
        ("緑地", "りょくち", "green tract of land / park", ["リョクチ"], []),
    ],
    # Lesson 175[cite: 44]
    [
        ("貿", "ぼう", "trade / exchange", ["ボウ"], []),
        ("貿易", "ぼうえき", "foreign trade", ["ボウエキ"], []),
        ("踊り", "おどり", "dance", ["ヨウ"], ["おど.り"]),
        ("封", "ふう", "seal / closing", ["フウ", "ホウ"], []),
        ("畳む", "たたむ", "to fold (clothes/futon)", ["ジョウ"], ["たた.む", "たたみ"]),
    ],
    # Lesson 176[cite: 44]
    [
        ("兆し", "きざし", "signs / omen / symptoms", ["チョウ"], ["きざ.し", "きざ.す"]),
        ("柱", "はしら", "pillar / post", ["チュウ"], ["はしら"]),
        ("電柱", "でんちゅう", "utility pole / telephone pole", ["デンチュウ"], []),
        ("駐", "ちゅう", "stop-over / reside / resident", ["チュウ"], []),
        ("兆候", "ちょうこう", "sign / indication / symptom", ["チョウコウ"], []),
    ],
    # Lesson 177[cite: 44]
    [
        ("駐車場", "ちゅうしゃじょう", "parking lot", ["チュウシャジョウ"], []),
        ("駐車違反", "ちゅうしゃいはん", "parking violation", ["チュウシャイハン"], []),
        ("祝う", "いわう", "to celebrate / congratulate", ["シュク", "シュウ"], ["いわ.う"]),
        ("お祝い", "おいわい", "congratulation / celebration / gift", ["シュク"], ["いわ.い"]),
        ("舞踊", "ぶよう", "dancing / dance", ["ブヨウ"], []),
    ],
    # Lesson 178[cite: 44]
    [
        ("祝日", "しゅくじつ", "national holiday", ["シュクジツ"], []),
        ("炭", "すみ", "charcoal / coal", ["タン"], ["すみ"]),
        ("石炭", "せきたん", "coal", ["セキタン"], []),
        ("柔らかい", "やわらかい", "soft / tender / supple", ["ジュウ", "ニュウ"], ["やわ.らかい"]),
        ("手腕", "しゅわん", "ability / capability / skill", ["シュワン"], []),
    ],
    # Lesson 179[cite: 44]
    [
        ("柔道", "じゅうどう", "judo", ["ジュウドウ"], []),
        ("雇う", "やとう", "to employ / hire", ["コ"], ["やと.う"]),
        ("乾く", "かわく", "to get dry", ["カン"], ["かわ.く", "かわ.かす"]),
        ("乾かす", "かわかす", "to dry (something)", ["カン"], ["かわ.かす"]),
        ("子守", "こもり", "babysitting / babysitter", [], ["こもり"]),
    ],
    # Lesson 180[cite: 44]
    [
        ("乾杯", "かんぱい", "cheers / toast", ["カンパイ"], []),
        ("鋭い", "するどい", "sharp / keen / acute", ["エイ"], ["するど.い"]),
        ("氷", "こおり", "ice", ["ヒョウ"], ["こおり", "ひ"]),
        ("隅", "すみ", "corner / nook", ["グウ"], ["すみ"]),
        ("鋭意", "えいい", "earnestly / diligently", ["エイイ"], []),
    ],
    # Lesson 181[cite: 44]
    [
        ("募る", "つのる", "to grow violent / invite / recruit", ["ボ"], ["つの.る"]),
        ("募集", "ぼしゅう", "recruitment / invitation", ["ボシュウ"], []),
        ("硬い", "かたい", "hard / solid / stiff", ["コウ"], ["かた.い"]),
        ("硬貨", "こうか", "coin", ["コウカ"], []),
        ("里山", "さとやま", "village-vicinity mountain / satoyama", [], ["さとやま"]),
    ],
    # Lesson 182[cite: 44]
    [
        ("塗る", "ぬる", "to paint / plaster / spread", ["ト"], ["ぬ.る"]),
        ("憎い", "にくい", "hateful / detestable", ["ゾウ"], ["にく.い", "にく.む"]),
        ("憎む", "にくむ", "to hate / detest", ["ゾウ"], ["にく.む"]),
        ("泥", "どろ", "mud / mire", ["デイ"], ["どろ"]),
        ("塗装", "とそう", "coating / painting", ["トソウ"], []),
    ],
    # Lesson 183[cite: 44]
    [
        ("泥棒", "どろぼう", "thief / burglar / robbery", ["ドロボウ"], []),
        ("脂", "あぶら", "fat / grease / lard", ["シ"], ["あぶら"]),
        ("粉", "こな", "flour / meal / powder", ["フン"], ["こ", "こな"]),
        ("詞", "し", "part of speech / words / poetry", ["シ"], []),
        ("台詞", "せりふ", "speech / lines / dialogue", [], ["せりふ"]),
    ],
    # Lesson 184[cite: 44]
    [
        ("名詞", "めいし", "noun", ["メイシ"], []),
        ("動詞", "どうし", "verb", ["ドウシ"], []),
        ("副詞", "ふくし", "adverb", ["フクシ"], []),
        ("形容詞", "けいようし", "adjective", ["ケイヨウシ"], []),
        ("憎悪", "ぞうお", "hatred / detestation", ["ゾウオ"], []),
    ],
    # Lesson 185[cite: 44]
    [
        ("代名詞", "だいめいし", "pronoun", ["ダイメイシ"], []),
        ("形容動詞", "けいようどうし", "na-adjective", ["ケイヨウドウシ"], []),
        ("筒", "つつ", "cylinder / pipe / tube", ["トウ"], ["つつ"]),
        ("封筒", "ふうとう", "envelope", ["フウトウ"], []),
        ("車窓", "しゃそう", "train/car window", ["シャソウ"], []),
    ],
    # Lesson 186[cite: 44]
    [
        ("掃く", "はく", "to sweep / brush", ["ソウ"], ["は.く"]),
        ("掃除", "そうじ", "cleaning / sweeping", ["ソウジ"], []),
        ("掃除機", "そうじき", "vacuum cleaner", ["ソウジキ"], []),
        ("塔", "とう", "tower / pagoda", ["トウ"], []),
        ("民放", "みんぽう", "commercial broadcasting", ["ミンポウ"], []),
    ],
    # Lesson 187[cite: 44]
    [
        ("賢い", "かしこい", "wise / clever / smart", ["ケン"], ["かしこ.い"]),
        ("拾う", "ひろう", "to pick up / find", ["シュウ", "ジュウ"], ["ひろ.う"]),
        ("麦", "むぎ", "wheat / barley / oats", ["バク"], ["むぎ"]),
        ("小麦", "こむぎ", "wheat", [], ["こむぎ"]),
        ("小麦粉", "こむぎこ", "wheat flour", [], ["こむぎこ"]),
    ],
    # Lesson 188[cite: 44]
    [
        ("刷る", "する", "to print", ["サツ"], ["す.る"]),
        ("印刷", "いんさつ", "printing", ["インサツ"], []),
        ("卵", "たまご", "egg", ["ラン"], ["たまご"]),
        ("械", "かい", "contraption / machine / instrument", ["カイ"], []),
        ("収拾", "しゅうしゅう", "control / bringing under control", ["シュウシュウ"], []),
    ],
    # Lesson 189[cite: 44]
    [
        ("機械", "きかい", "machine / mechanism", ["キカイ"], []),
        ("祈り", "いのり", "prayer / supplication", ["キ"], ["いの.り"]),
        ("祈る", "いのる", "to pray / wish", ["キ"], ["いの.る"]),
        ("灰", "はい", "ash / ashes", ["カイ"], ["はい"]),
        ("祈願", "きがん", "prayer / supplication", ["キガン"], []),
    ],
    # Lesson 190[cite: 44]
    [
        ("灰皿", "はいざら", "ashtray", [], ["はいざら"]),
        ("灰色", "はいいろ", "gray / ash color", [], ["はいいろ"]),
        ("召す", "めす", "to call / eat / wear (honorific)", ["ショウ"], ["め.す"]),
        ("召し上がる", "めしあがる", "to eat / drink (honorific)", [], ["めしあ.がる"]),
        ("召集", "しょうしゅう", "convening / calling together", ["ショウシュウ"], []),
    ],
    # Lesson 191[cite: 45]
    [
        ("溶く", "とく", "to dissolve / melt", ["ヨウ"], ["と.ける", "と.かす", "と.く"]),
        ("溶ける", "とける", "to melt / thaw / dissolve", ["ヨウ"], ["と.ける"]),
        ("溶かす", "とかす", "to melt / dissolve", ["ヨウ"], ["と.かす"]),
        ("溶岩", "ようがん", "lava", ["ヨウガン"], []),
        ("日和", "ひより", "weather / fair weather", [], ["ひより"]),
    ],
    # Lesson 192[cite: 45]
    [
        ("溶け込む", "とけこむ", "to melt into / blend in", [], ["とけこ.む"]),
        ("磨く", "みがく", "to polish / shine / brush (teeth)", ["マ"], ["みが.く"]),
        ("粒", "つぶ", "grain / drop / particle", ["リュウ"], ["つぶ"]),
        ("喫する", "きっする", "to smoke / drink / eat", ["キツ"], ["きっ.する"]),
        ("粒子", "りゅうし", "particle / grain", ["リュウシ"], []),
    ],
    # Lesson 193[cite: 45]
    [
        ("喫茶店", "きっさてん", "coffee shop / cafe", ["キッサテン"], []),
        ("机", "つくえ", "desk", ["キ"], ["つくえ"]),
        ("貯まる", "たまる", "to accumulate / be saved", ["チョ"], ["た.まる", "た.める"]),
        ("貯める", "ためる", "to save up (money)", ["チョ"], ["た.める"]),
        ("喫煙", "きつえん", "smoking", ["キツエン"], []),
    ],
    # Lesson 194[cite: 45]
    [
        ("貯金", "ちょきん", "savings / deposit", ["チョキン"], []),
        ("匹", "ひき", "counter for small animals", ["ヒツ"], ["ひき"]),
        ("綿", "めん", "cotton", ["メン"], ["わた"]),
        ("綿", "わた", "cotton / padding", ["メン"], ["わた"]),
        ("声高", "こわだか", "loud voice", [], ["こわだか"]),
    ],
    # Lesson 195[cite: 45]
    [
        ("木綿", "もめん", "cotton (material)", ["モメン"], []),
        ("贈る", "おくる", "to give (as a gift) / present", ["ゾウ", "ソウ"], ["おく.る"]),
        ("贈り物", "おくりもの", "present / gift", [], ["おくりもの"]),
        ("凍る", "こおる", "to freeze / be frozen", ["トウ"], ["こお.る", "こご.える"]),
        ("贈与", "ぞうよ", "donation / presentation", ["ゾウヨ"], []),
    ],
    # Lesson 196[cite: 45]
    [
        ("冷凍", "れいとう", "freezing / refrigeration", ["レイトウ"], []),
        ("冷凍食品", "れいとうしょくひん", "frozen food", ["レイトウショクヒン"], []),
        ("瓶", "びん", "bottle / jar", ["ビン"], []),
        ("花瓶", "かびん", "flower vase", ["カビン"], []),
        ("賛否", "さんぴ", "yes or no / pros and cons", ["サンピ"], []),
    ],
    # Lesson 197[cite: 45]
    [
        ("帽", "ぼう", "cap / headgear", ["ボウ"], []),
        ("帽子", "ぼうし", "hat / cap", ["ボウシ"], []),
        ("涼しい", "すずしい", "cool / refreshing", ["リョウ"], ["すず.しい", "すず.む"]),
        ("秒", "びょう", "second (time)", ["ビョウ"], []),
        ("顔写真", "かおじゃしん", "ID photo / portrait photo", [], ["かおじゃしん"]),
    ],
    # Lesson 198[cite: 45]
    [
        ("湿る", "しめる", "to become damp / get wet", ["シツ"], ["しめ.る", "しめ.す"]),
        ("湿度", "しつど", "humidity", ["シツド"], []),
        ("湿気", "しっけ", "moisture / humidity / dampness", ["シッケ"], []),
        ("湿度計", "しつどけい", "hygrometer", ["シツドケイ"], []),
        ("群馬", "ぐんま", "Gunma Prefecture", ["グンマ"], []),
    ],
    # Lesson 199[cite: 45]
    [
        ("蒸す", "むす", "to steam / be humid", ["ジョウ"], ["む.す", "む.れる"]),
        ("菓", "か", "candy / cakes / fruit", ["カ"], []),
        ("お菓子", "おかし", "sweets / candy / snacks", ["カシ"], []),
        ("耕す", "たがやす", "to till / plow / cultivate", ["コウ"], ["たがや.す"]),
        ("蒸気", "じょうき", "steam / vapor", ["ジョウキ"], []),
    ],
    # Lesson 200[cite: 45]
    [
        ("耕地", "こうち", "arable land / cultivated land", ["コウチ"], []),
        ("ウラン鉱", "ウランこう", "uranium ore", ["コウ"], []),
        ("鉱物", "こうぶつ", "mineral", ["コウブツ"], []),
        ("炭鉱", "たんこう", "coal mine", ["タンコウ"], []),
        ("宅急便", "たっきゅうびん", "express home delivery", ["タッキュウビン"], []),
    ],
    # Lesson 201[cite: 46]
    [
        ("膚", "はだ", "skin / body / grain", ["フ"], ["はだ"]),
        ("皮膚", "ひふ", "skin", ["ヒフ"], []),
        ("胃", "い", "stomach", ["イ"], []),
        ("胃痛", "いつう", "stomachache", ["イツウ"], []),
        ("吹雪", "ふぶき", "snowstorm / blizzard", [], ["ふぶき"]),
    ],
    # Lesson 202[cite: 46]
    [
        ("挟む", "はさむ", "to hold between / pinch / insert", ["キョウ"], ["はさ.む", "はさ.まる"]),
        ("挟まる", "はさまる", "to get caught between", ["キョウ"], ["はさ.まる"]),
        ("郊", "こう", "outskirts / suburbs", ["コウ"], []),
        ("郊外", "こうがい", "suburb / outskirts", ["コウガイ"], []),
        ("更ける", "ふける", "to grow late (night)", ["コウ"], ["ふ.ける", "ふ.かす"]),
    ],
    # Lesson 203[cite: 46]
    [
        ("銅", "どう", "copper", ["ドウ"], []),
        ("銅貨", "どうか", "copper coin", ["ドウカ"], []),
        ("鈍い", "にぶい", "dull / blunt / slow", ["ドン"], ["にぶ.い", "にぶ.る"]),
        ("缶", "かん", "can / tin", ["カン"], []),
        ("強者", "つわもの", "strong person / veteran", [], ["つわもの"]),
    ],
    # Lesson 204[cite: 46]
    [
        ("缶詰", "かんづめ", "canned food / tinned goods", [], ["かんづめ"]),
        ("空き缶", "あきかん", "empty can", [], ["あきかん"]),
        ("枯れる", "かれる", "to wither / die (plant)", ["コ"], ["か.れる", "か.らす"]),
        ("滴", "しずく", "drop (of water)", ["テキ"], ["しずく", "したた.る"]),
        ("父兄", "ふけい", "parents and older brothers / guardians", ["フケイ"], []),
    ],
    # Lesson 205[cite: 46]
    [
        ("水滴", "すいてき", "drop of water", ["スイテキ"], []),
        ("符", "ふ", "token / sign / mark / tally", ["フ"], []),
        ("切符", "きっぷ", "ticket", ["キップ"], []),
        ("軟らかい", "やわらかい", "soft / tender / pliable", ["ナン"], ["やわ.らかい"]),
        ("逆行", "ぎゃっこう", "retrogression / going backward", ["ギャッコウ"], []),
    ],
    # Lesson 206[cite: 46]
    [
        ("濯ぐ", "すすぐ", "to rinse / wash out", ["タク"], ["すす.ぐ"]),
        ("洗濯", "せんたく", "washing / laundry", ["センタク"], []),
        ("洗濯物", "せんたくもの", "laundry / clothes to be washed", ["センタクモノ"], []),
        ("洗濯機", "せんたくき", "washing machine", ["センタクキ"], []),
        ("徳島", "とくしま", "Tokushima Prefecture", [], ["とくしま"]),
    ],
    # Lesson 207[cite: 46]
    [
        ("伺う", "うかがう", "to visit / ask / inquire (humble)", ["シ"], ["うかが.う"]),
        ("沸く", "わく", "to boil / grow hot", ["フツ"], ["わ.く", "わ.かす"]),
        ("沸かす", "わかす", "to boil / heat", ["フツ"], ["わ.かす"]),
        ("曇り", "くもり", "cloudiness / cloudy weather", ["ドン"], ["くも.り"]),
        ("机上", "きじょう", "on the desk / theoretical", ["キジョウ"], []),
    ],
    # Lesson 208[cite: 46]
    [
        ("曇る", "くもる", "to get cloudy / fog up", ["ドン"], ["くも.る"]),
        ("肯", "こう", "agreement / consent", ["コウ"], []),
        ("肯定", "こうてい", "affirmation / confirmation", ["コウテイ"], []),
        ("燥ぐ", "はしゃぐ", "to make merry / frolic", ["ソウ"], ["はしゃ.ぐ"]),
        ("死神", "しにがみ", "god of death / Grim Reaper", [], ["しにがみ"]),
    ],
    # Lesson 209[cite: 46]
    [
        ("乾燥", "かんそう", "dryness / dehydration", ["カンソウ"], []),
        ("乾燥機", "かんそうき", "clothes dryer / dehydrator", ["カンソウキ"], []),
        ("零", "れい", "zero / nought", ["レイ"], []),
        ("零点", "れいてん", "zero points / failing mark", ["レイテン"], []),
        ("首富", "しゅふ", "richest person", ["シュフ"], []),
    ],
    # Lesson 210[cite: 46]
    [
        ("十階", "じゅっかい", "tenth floor", ["ジュッカイ"], []),
        ("九階", "きゅうかい", "ninth floor", ["キュウカイ"], []),
        ("八階", "はっかい", "eighth floor", ["ハッカイ"], []),
        ("七階", "ななかい", "seventh floor", ["ナナカイ"], []),
        ("和菓子", "わがし", "traditional Japanese sweets", ["ワガシ"], []),
    ],
    # Lesson 211[cite: 46]
    [
        ("六階", "ろっかい", "sixth floor", ["ロッカイ"], []),
        ("五階", "ごかい", "fifth floor", ["ゴカイ"], []),
        ("四階", "よんかい", "fourth floor", ["ヨンカイ"], []),
        ("三階", "さんがい", "third floor", ["サンガイ"], []),
        ("読解", "どっかい", "reading comprehension", ["ドッカイ"], []),
    ],
    # Lesson 212[cite: 46]
    [
        ("二階", "にかい", "second floor", ["ニカイ"], []),
        ("一階", "いっかい", "first floor / ground floor", ["イッカイ"], []),
        ("一冊", "いっさつ", "one book / one volume", ["イッサツ"], []),
        ("二冊", "にさつ", "two books", ["ニサツ"], []),
        ("香川", "かがわ", "Kagawa Prefecture", [], ["かがわ"]),
    ],
    # Lesson 213[cite: 46]
    [
        ("三冊", "さんさつ", "three books", ["サンサツ"], []),
        ("四冊", "よんさつ", "four books", ["ヨンサツ"], []),
        ("五冊", "ごさつ", "five books", ["ゴサツ"], []),
        ("六冊", "ろくさつ", "six books", ["ロクサツ"], []),
        ("凍える", "こごえる", "to freeze / be chilled", ["トウ"], ["こご.える"]),
    ],
    # Lesson 214[cite: 46]
    [
        ("七冊", "ななさつ", "seven books", ["ナナサツ"], []),
        ("八冊", "はっさつ", "eight books", ["ハッサツ"], []),
        ("九冊", "きゅうさつ", "nine books", ["キュウサツ"], []),
        ("十冊", "じゅっさつ", "ten books", ["ジュッサツ"], []),
        ("山積み", "やまづみ", "huge pile / heap", [], ["やまづみ"]),
    ],
    # Lesson 215[cite: 46]
    [
        ("何冊", "なんさつ", "how many books", ["ナンサツ"], []),
        ("二枚", "にまい", "two sheets/flat objects", ["ニマイ"], []),
        ("三枚", "さんまい", "three sheets/flat objects", ["サンマイ"], []),
        ("四枚", "よんまい", "four sheets/flat objects", ["ヨンマイ"], []),
        ("延伸", "えんしん", "extension / elongation", ["エンシン"], []),
    ],
    # Lesson 216[cite: 46]
    [
        ("六枚", "ろくまい", "six sheets/flat objects", ["ロクマイ"], []),
        ("七枚", "ななまい", "seven sheets/flat objects", ["ナナマイ"], []),
        ("八枚", "はちまい", "eight sheets/flat objects", ["ハチマイ"], []),
        ("坂", "さか", "slope / hill", ["ハン"], ["さか"]),
        ("坂道", "さかみち", "sloping road / hill", [], ["さかみち"]),
    ],
    # Lesson 217[cite: 46]
    [
        ("九枚", "きゅうまい", "nine sheets/flat objects", ["キュウマイ"], []),
        ("十枚", "じゅうまい", "ten sheets/flat objects", ["ジュウマイ"], []),
        ("何枚", "なんまい", "how many sheets/flat objects", ["ナンマイ"], []),
        ("畜", "ちく", "livestock / domestic fowl", ["チク"], []),
        ("妻", "つま", "wife", ["サイ"], ["つま"]),
    ],
    # Lesson 218[cite: 46]
    [
        ("花園", "はなぞの", "flower garden", [], ["はなぞの"]),
        ("前倒し", "まえだおし", "bringing forward (schedule)", [], ["まえだおし"]),
        ("採点", "さいてん", "grading / marking / scoring", ["サイテン"], []),
        ("四捨五入", "ししゃごにゅう", "rounding off (numbers)", ["シシャゴニュウ"], []),
        ("無言", "むごん", "silence / saying nothing", ["ムゴン"], []),
    ],
    # Lesson 219[cite: 46]
    [
        ("お買い得", "おかいどく", "good buy / bargain", [], ["おかいどく"]),
        ("三位一体", "さんみいったい", "Trinity / three-in-one", ["サンミイッタイ"], []),
        ("見出す", "みいだす", "to find out / discover", [], ["みいだ.す"]),
        ("手放し", "てばなし", "hands-free / unreserved", [], ["てばなし"]),
        ("税抜", "ぜいぬき", "tax excluded", ["ゼイヌキ"], []),
    ],
    # Lesson 220[cite: 46]
    [
        ("海老", "えび", "shrimp / prawn / lobster", [], ["えび"]),
        ("注す", "さす", "to pour / add / drop (eye drops)", ["チュウ"], ["さ.す"]),
        ("足下", "あしもと", "at one's feet / underfoot", [], ["あしもと"]),
        ("治める", "おさめる", "to govern / manage / subdue", ["チ", "ジ"], ["おさ.める"]),
        ("個所", "かしょ", "place / point / passage", ["カショ"], []),
    ],
    # Lesson 221[cite: 46]
    [
        ("点く", "つく", "to be lit / catch fire / turn on", ["テン"], ["つ.く", "つ.ける"]),
        ("撮る", "とる", "to take (a photo) / record", ["サツ"], ["と.る"]),
        ("恐い", "こわい", "scary / frightening", ["キョウ"], ["こわ.い"]),
        ("美味い", "うまい", "delicious / tasty / skillful", ["ビミ"], ["うま.い"]),
    ],
    # Lesson 222[cite: 46]
    [
        ("想う", "おもう", "to think / feel / imagine", ["ソウ", "ソ"], ["おも.う"]),
        ("寝転がる", "ねころがる", "to lie down / sprawl out", [], ["ねころ.がる"]),
        ("灯り", "あかり", "light / lamp", ["トウ"], ["あ.かり"]),
        ("ゴミ箱", "ゴミばこ", "trash can / garbage bin", [], ["ゴミばこ"]),
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
    if not os.path.exists(PART1_JSON_PATH):
        raise FileNotFoundError(f"Run 'python generate_n2_part1.py' first to create {PART1_JSON_PATH}.")

    with open(PART1_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N2_PART2_DATA):
        lesson_num = 116 + l_idx
        lesson_items = []

        for word, kana, meaning, onyomi, kunyomi in chunk:
            characters_data = []
            for ch in word:
                characters_data.append({
                    "char": ch,
                    "strokes": get_strokes_for_char(ch),
                })

            lesson_items.append({
                "id": f"n2-{item_counter}",
                "level": "N2",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n2-lesson-{lesson_num}",
            "level": "N2",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    os.makedirs(os.path.dirname(OUTPUT_TS_PATH), exist_ok=True)
    ts_content = (
        "import type { KanjiLesson } from '../types/kanji';\n\n"
        f"export const N2_LESSONS: KanjiLesson[] = {json.dumps(lessons, ensure_ascii=False, indent=2)};\n"
    )

    with open(OUTPUT_TS_PATH, "w", encoding="utf-8") as f:
        f.write(ts_content)

    os.remove(PART1_JSON_PATH)
    print(f"Done! Compiled all {len(lessons)} N2 lessons ({item_counter - 1} items) into {OUTPUT_TS_PATH}.")


if __name__ == "__main__":
    main()