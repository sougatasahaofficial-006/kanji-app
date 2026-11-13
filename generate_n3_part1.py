import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n3_part1.json"

N3_PART1_DATA = [
    # Lesson 1[cite: 16]
    [
        ("笑う", "わらう", "to laugh / smile", ["ショウ"], ["わら.う", "え.む"]),
        ("王", "おう", "king", ["オウ"], []),
        ("王子", "おうじ", "prince", ["オウジ"], []),
        ("女王", "じょおう", "queen", ["ジョオウ"], []),
        ("有る", "ある", "to exist / have", ["ユウ", "ウ"], ["あ.る"]),
    ],
    # Lesson 2[cite: 16]
    [
        ("部", "ぶ", "department / club / part", ["ブ"], []),
        ("学部", "がくぶ", "university faculty", ["ガクブ"], []),
        ("部下", "ぶか", "subordinate", ["ブカ"], []),
        ("部分", "ぶぶん", "portion / section", ["ブブン"], []),
        ("下さる", "くださる", "to give (honorific)", ["カ", "ゲ"], ["くだ.さる"]),
    ],
    # Lesson 3[cite: 16]
    [
        ("部長", "ぶちょう", "department head", ["ブチョウ"], []),
        ("部屋", "へや", "room", [], ["へや"]),
        ("彼", "かれ", "he / boyfriend", ["ヒ"], ["かれ", "かの"]),
        ("彼ら", "かれら", "they", ["ヒ"], ["かれら"]),
        ("会", "かい", "meeting / association", ["カイ", "エ"], ["あ.う"]),
    ],
    # Lesson 4[cite: 16]
    [
        ("彼女", "かのじょ", "she / girlfriend", [], ["かのじょ"]),
        ("内", "うち", "inside / within", ["ナイ", "ダイ"], ["うち"]),
        ("国内", "こくない", "domestic / within the country", ["コクナイ"], []),
        ("以内", "いない", "within / less than", ["イナイ"], []),
        ("人間", "にんげん", "human being", ["ニンゲン"], []),
    ],
    # Lesson 5[cite: 16]
    [
        ("内部", "ないぶ", "interior / inside", ["ナイブ"], []),
        ("実は", "じつは", "actually / to tell the truth", ["ジツ"], []),
        ("実力", "じつりょく", "real ability / merit", ["ジツリョク"], []),
        ("大", "だい", "large / big", ["ダイ", "タイ"], ["おお.きい"]),
        ("先ず", "まず", "first of all", ["セン"], ["ま.ず"]),
    ],
    # Lesson 6[cite: 16]
    [
        ("実習", "じっしゅう", "practical training", ["ジッシュウ"], []),
        ("当たる", "あたる", "to hit / be right", ["トウ"], ["あ.たる", "あ.てる"]),
        ("当時", "とうじ", "at that time", ["トウジ"], []),
        ("本当", "ほんとう", "truth / reality", ["ホントウ"], []),
        ("生", "なま", "raw / fresh / live", ["セイ", "ショウ"], ["なま", "い.きる"]),
    ],
    # Lesson 7[cite: 16]
    [
        ("本当に", "ほんとうに", "really / truly", ["ホントウ"], []),
        ("日当たり", "ひあたり", "sunlight exposure", [], ["ひあたり"]),
        ("当たり前", "あたりまえ", "natural / obvious", [], ["あたりまえ"]),
        ("戦う", "たたかう", "to fight / battle", ["セン"], ["たたか.う", "いくさ"]),
        ("笑い", "わらい", "laughter / smile", ["ショウ"], ["わら.い"]),
    ],
    # Lesson 8[cite: 16]
    [
        ("戦い", "たたかい", "battle / fight", ["セン"], ["たたか.い"]),
        ("大戦", "たいせん", "great war", ["タイセン"], []),
        ("亡くなる", "なくなる", "to pass away / die", ["ボウ", "モウ"], ["な.くなる"]),
        ("忙しい", "いそがしい", "busy", ["ボウ"], ["いそが.しい"]),
        ("行ける", "いける", "can go / be good", ["コウ"], ["い.ける"]),
    ],
    # Lesson 9[cite: 16]
    [
        ("性", "せい", "gender / nature", ["セイ", "ショウ"], ["さが"]),
        ("女性", "じょせい", "woman / female", ["ジョセイ"], []),
        ("男性", "だんせい", "man / male", ["ダンセイ"], []),
        ("性別", "せいべつ", "sex / gender", ["セイベツ"], []),
        ("小", "しょう", "small / little", ["ショウ"], ["ちい.さい", "こ"]),
    ],
    # Lesson 10[cite: 16]
    [
        ("対", "たい", "versus / opposite / pair", ["タイ", "ツイ"], []),
        ("対する", "たいする", "to face / confront", ["タイ"], []),
        ("関する", "かんする", "to concern / be related to", ["カン"], []),
        ("関心", "かんしん", "concern / interest", ["カンシン"], []),
        ("明らか", "あきらか", "clear / obvious", ["メイ"], ["あき.らか"]),
    ],
    # Lesson 11[cite: 16]
    [
        ("無関心", "むかんしん", "indifference / apathy", ["ムカンシン"], []),
        ("感じる", "かんじる", "to feel / sense", ["カン"], ["かん.じる"]),
        ("感動", "かんどう", "deep emotion / excitement", ["カンドウ"], []),
        ("感心", "かんしん", "admiration", ["カンシン"], []),
        ("感じ", "かんじ", "feeling / impression", ["カン"], ["かん.じ"]),
    ],
    # Lesson 12[cite: 16]
    [
        ("定まる", "さだまる", "to be decided / settled", ["テイ", "ジョウ"], ["さだ.まる"]),
        ("定員", "ていいん", "fixed capacity / quota", ["テイイン"], []),
        ("一定", "いってい", "fixed / constant / certain", ["イッテイ"], []),
        ("定食", "ていしょく", "set meal", ["テイショク"], []),
        ("用いる", "もちいる", "to use / employ", ["ヨウ"], ["もち.いる"]),
    ],
    # Lesson 13[cite: 16]
    [
        ("定休日", "ていきゅうび", "regular holiday", ["テイキュウビ"], []),
        ("不安定", "ふあんてい", "instability / unstable", ["フアンテイ"], []),
        ("合う", "あう", "to fit / match", ["ゴウ", "ガッ"], ["あ.う"]),
        ("合わせる", "あわせる", "to combine / adjust", ["ゴウ"], ["あ.わせる"]),
        ("関わる", "かかわる", "to be involved / affected", ["カン"], ["かか.わる"]),
    ],
    # Lesson 14[cite: 17]
    [
        ("場合", "ばあい", "case / situation", [], ["ばあい"]),
        ("試合", "しあい", "match / game", ["シアイ"], []),
        ("合図", "あいず", "sign / signal", ["アイズ"], []),
        ("集合", "しゅうごう", "gathering / assembly", ["シュウゴウ"], []),
        ("土地", "とち", "land / plot", ["トチ"], []),
    ],
    # Lesson 15[cite: 17]
    [
        ("見合い", "みあい", "arranged marriage interview", [], ["みあい"]),
        ("間に合う", "まにあう", "to be in time", [], ["まにあ.う"]),
        ("口に合う", "くちにあう", "to suit one's taste", [], ["くちにあ.う"]),
        ("知り合う", "しりあう", "to get to know each other", [], ["しりあ.う"]),
        ("新た", "あらた", "new / fresh", ["シン"], ["あら.た"]),
    ],
    # Lesson 16[cite: 17]
    [
        ("話し合い", "はなしあい", "discussion / talk", [], ["はなしあい"]),
        ("話し合う", "はなしあう", "to discuss / talk together", [], ["はなしあ.う"]),
        ("待ち合わせ", "まちあわせ", "meeting up / appointment", [], ["まちあわせ"]),
        ("問い合わせ", "といあわせ", "inquiry / question", [], ["といあわせ"]),
        ("学ぶ", "まなぶ", "to study / learn", ["ガク"], ["まな.ぶ"]),
    ],
    # Lesson 17[cite: 17]
    [
        ("待ち合わせる", "まちあわせる", "to meet up", [], ["まちあ.わせる"]),
        ("問い合わせる", "といあわせる", "to inquire / ask", [], ["といあ.わせる"]),
        ("政", "まつりごと", "politics / government", ["セイ", "ショウ"], ["まつりごと"]),
        ("取る", "とる", "to take / pick up", ["シュ"], ["と.る"]),
        ("食う", "くう", "to eat (casual/rough)", ["ショク"], ["く.う"]),
    ],
    # Lesson 18[cite: 17]
    [
        ("ちり取り", "ちりとり", "dustpan", [], ["ちりとり"]),
        ("聞き取り", "ききとり", "listening comprehension", [], ["ききとり"]),
        ("年を取る", "としをとる", "to grow old", [], ["としをと.る"]),
        ("取り出す", "とりだす", "to take out", [], ["とりだ.す"]),
        ("左右", "さゆう", "left and right", ["サユウ"], []),
    ],
    # Lesson 19[cite: 17]
    [
        ("聞き取る", "ききとる", "to catch / hear", [], ["ききと.る"]),
        ("所", "ところ", "place / spot", ["ショ"], ["ところ"]),
        ("近所", "きんじょ", "neighborhood", ["キンジョ"], []),
        ("台所", "だいどころ", "kitchen", [], ["だいどころ"]),
        ("死亡", "しぼう", "death / mortality", ["シボウ"], []),
    ],
    # Lesson 20[cite: 17]
    [
        ("場所", "ばしょ", "place / location", ["バショ"], []),
        ("長所", "ちょうしょ", "strong point / merit", ["チョウショ"], []),
        ("住所", "じゅうしょ", "address", ["ジュウショ"], []),
        ("現れる", "あらわれる", "to appear / emerge", ["ゲン"], ["あらわ.れる"]),
        ("青年", "せいねん", "youth / young person", ["セイネン"], []),
    ],
    # Lesson 21[cite: 17]
    [
        ("現場", "げんば", "actual spot / scene", ["ゲンバ", "ゲンジョウ"], []),
        ("現代", "げんだい", "modern times", ["ゲンダイ"], []),
        ("現実", "げんじつ", "reality", ["ゲンジツ"], []),
        ("現金", "げんきん", "cash", ["ゲンキン"], []),
        ("出来事", "できごと", "incident / event", [], ["できごと"]),
    ],
    # Lesson 22[cite: 17]
    [
        ("現代人", "げんだいじん", "modern person", ["ゲンダイジン"], []),
        ("現実的", "げんじつてき", "realistic / practical", ["ゲンジツテキ"], []),
        ("現代的", "げんだいてき", "modern / contemporary", ["ゲンダイテキ"], []),
        ("工事現場", "こうじげんば", "construction site", ["コウジゲンバ"], []),
        ("主に", "おもに", "mainly / primarily", ["シュ"], ["おも.に"]),
    ],
    # Lesson 23[cite: 17]
    [
        ("最も", "もっとも", "most / extremely", ["サイ"], ["もっと.も"]),
        ("最中", "さいちゅう", "in the middle of", ["サイチュウ"], []),
        ("最大", "さいだい", "greatest / largest", ["サイダイ"], []),
        ("最後", "さいご", "last / end", ["サイゴ"], []),
        ("世間", "せけん", "world / society / public", ["セケン"], []),
    ],
    # Lesson 24[cite: 17]
    [
        ("最小", "さいしょう", "smallest / minimum", ["サイショウ"], []),
        ("最多", "さいた", "most numerous", ["サイタ"], []),
        ("最少", "さいしょう", "fewest / least", ["サイショウ"], []),
        ("最悪", "さいあく", "the worst", ["サイアク"], []),
        ("明かり", "あかり", "light / lamp", ["メイ"], ["あ.かり"]),
    ],
    # Lesson 25[cite: 17]
    [
        ("最新", "さいしん", "latest / newest", ["サイシン"], []),
        ("最近", "さいきん", "recently / lately", ["サイキン"], []),
        ("最高", "さいこう", "highest / supreme / best", ["サイコウ"], []),
        ("化する", "かする", "to change into / transform", ["カ", "ケ"], ["ば.ける"]),
        ("手当", "てあて", "allowance / medical treatment", [], ["てあて"]),
    ],
    # Lesson 26[cite: 17]
    [
        ("文化", "ぶんか", "culture", ["ブンカ"], []),
        ("悪化", "あっか", "worsening / deterioration", ["アッカ"], []),
        ("少子化", "しょうしか", "declining birthrate", ["ショウシカ"], []),
        ("民", "たみ", "people / citizens", ["ミン"], ["たみ"]),
        ("親父", "おやじ", "one's father / old man", [], ["おやじ"]),
    ],
    # Lesson 27[cite: 17]
    [
        ("国民", "こくみん", "citizen / nation", ["コクミン"], []),
        ("相", "そう", "aspect / phase / mutual", ["ソウ", "ショウ"], ["あい"]),
        ("相手", "あいて", "companion / partner / opponent", ["アイテ"], []),
        ("相当", "そうとう", "considerable / equivalent", ["ソウトウ"], []),
        ("半ば", "なかば", "middle / half", ["ハン"], ["なか.ば"]),
    ],
    # Lesson 28[cite: 17]
    [
        ("法", "ほう", "law / method", ["ホウ", "ハッ"], []),
        ("文法", "ぶんぽう", "grammar", ["ブンポウ"], []),
        ("方法", "ほうほう", "method / way", ["ホウホウ"], []),
        ("法学", "ほうがく", "jurisprudence / law study", ["ホウガク"], []),
        ("弟子", "でし", "pupil / apprentice", ["デシ"], []),
    ],
    # Lesson 29[cite: 17]
    [
        ("全て", "すべて", "all / everything", ["ゼン"], ["すべ.て", "まった.く"]),
        ("全く", "まったく", "entirely / completely", ["ゼン"], ["まった.く"]),
        ("全体", "ぜんたい", "whole / entirety", ["ゼンタイ"], []),
        ("全部", "ぜんぶ", "all / entire", ["ゼンブ"], []),
        ("北部", "ほくぶ", "northern part", ["ホクブ"], []),
    ],
    # Lesson 30[cite: 18]
    [
        ("安全", "あんぜん", "safety / security", ["アンゼン"], []),
        ("全部で", "ぜんぶで", "in total", ["ゼンブ"], []),
        ("全体的", "ぜんたいてき", "overall / general", ["ゼンタイテキ"], []),
        ("全国的", "ぜんこくてき", "nationwide", ["ゼンコクテキ"], []),
        ("黒人", "こくじん", "Black person", ["コクジン"], []),
    ],
    # Lesson 31[cite: 18]
    [
        ("安全運転", "あんぜんうんてん", "safe driving", ["アンゼンウンテン"], []),
        ("情", "じょう", "feeling / emotion / sympathy", ["ジョウ", "セイ"], ["なさ.け"]),
        ("友情", "ゆうじょう", "friendship", ["ユウジョウ"], []),
        ("感情", "かんじょう", "emotion / feeling", ["カンジョウ"], []),
        ("手作り", "てづくり", "handmade", [], ["てづくり"]),
    ],
    # Lesson 32[cite: 18]
    [
        ("感情的", "かんじょうてき", "emotional", ["カンジョウテキ"], []),
        ("向こう", "むこう", "over there / opposite side", ["コウ"], ["む.こう"]),
        ("向かう", "むかう", "to face / head toward", ["コウ"], ["む.かう"]),
        ("方向", "ほうこう", "direction / course", ["ホウコウ"], []),
        ("情けない", "なさけない", "miserable / pitiful", ["ジョウ"], ["なさ.けない"]),
    ],
    # Lesson 33[cite: 18]
    [
        ("平ら", "たいら", "flat / level", ["ヘイ", "ビョウ"], ["たい.ら", "ひら"]),
        ("平日", "へいじつ", "weekday", ["ヘイジツ"], []),
        ("平気", "へいき", "cool / calm / unconcerned", ["ヘイキ"], []),
        ("成る", "なる", "to become / consist of", ["セイ", "ジョウ"], ["な.る"]),
        ("相性", "あいしょう", "compatibility", ["アイショウ"], []),
    ],
    # Lesson 34[cite: 18]
    [
        ("成田", "なりた", "Narita", [], ["なりた"]),
        ("成長", "せいちょう", "growth / development", ["セイチョウ"], []),
        ("成人の日", "せいじんのひ", "Coming of Age Day", ["セイジン"], []),
        ("経つ", "たつ", "to pass / elapse (time)", ["ケイ", "キョウ"], ["た.つ", "へ.る"]),
        ("経験", "けいけん", "experience", ["ケイケン"], []),
    ],
    # Lesson 35[cite: 18]
    [
        ("信じる", "しんじる", "to believe / trust", ["シン"], ["しん.じる"]),
        ("自信", "じしん", "self-confidence", ["ジシン"], []),
        ("送信", "そうしん", "transmission / sending", ["ソウシン"], []),
        ("信用", "しんよう", "trust / credit", ["シンヨウ"], []),
        ("心地よい", "ここちよい", "comfortable / pleasant", [], ["ここちよい"]),
    ],
    # Lesson 36[cite: 18]
    [
        ("面", "めん", "face / surface / aspect", ["メン"], ["おも", "おもて", "つら"]),
        ("正面", "しょうめん", "front / facade", ["ショウメン"], []),
        ("画面", "がめん", "screen", ["ガメン"], []),
        ("面白い", "おもしろい", "interesting / funny", [], ["おもしろ.い"]),
        ("文字通り", "もじどおり", "literally", ["モジ"], []),
    ],
    # Lesson 37[cite: 18]
    [
        ("真面目", "まじめ", "serious / earnest", ["シンメンモク"], ["まじめ"]),
        ("不真面目", "ふまじめ", "insincere / frivolous", ["フマジメ"], []),
        ("込む", "こむ", "to be crowded / go into", [], ["こ.む", "こ.める"]),
        ("止す", "よす", "to stop / give up", ["シ"], ["よ.す"]),
    ],
    # Lesson 38[cite: 18]
    [
        ("連れる", "つれる", "to lead / take along", ["レン"], ["つ.れる", "つら.なる"]),
        ("連れてくる", "つれてくる", "to bring someone along", ["レン"], ["つ.れてくる"]),
        ("連休", "れんきゅう", "consecutive holidays", ["レンキュウ"], []),
        ("万全", "ばんぜん", "perfection / thoroughness", ["バンゼン"], []),
        ("自力", "じりき", "one's own strength", ["ジリキ"], []),
    ],
    # Lesson 39[cite: 18]
    [
        ("連れて行く", "つれていく", "to take someone along", ["レン"], ["つ.れていく"]),
        ("原", "はら", "field / plain / origin", ["ゲン"], ["はら"]),
        ("原料", "げんりょう", "raw materials", ["ゲンリョウ"], []),
        ("顔", "かお", "face", ["ガン"], ["かお"]),
        ("お部屋", "おへや", "room (polite)", [], ["へや"]),
    ],
    # Lesson 40[cite: 18]
    [
        ("顔色", "かおいろ", "complexion / expression", ["ガンショク"], ["かおいろ"]),
        ("笑顔", "えがお", "smiling face", [], ["えがお"]),
        ("機", "き", "opportunity / machine", ["キ"], ["はた"]),
        ("機会", "きかい", "chance / opportunity", ["キカイ"], []),
        ("七夕", "たなばた", "Star Festival (Tanabata)", [], ["たなばた"]),
    ],
    # Lesson 41[cite: 18]
    [
        ("欠ける", "かける", "to be lacking / chipped", ["ケツ"], ["か.ける", "か.く"]),
        ("次に", "つぎに", "next / secondly", ["ジ"], ["つぎ"]),
        ("次の", "つぎの", "next / following", ["ジ"], ["つぎ"]),
        ("次女", "じじょ", "second daughter", ["ジジョ"], []),
        ("次", "つぎ", "next", ["ジ", "シ"], ["つ.ぐ", "つぎ"]),
    ],
    # Lesson 42[cite: 18]
    [
        ("次男", "じなん", "second son", ["ジナン"], []),
        ("お米", "おこめ", "rice", ["ベイ", "マイ"], ["こめ"]),
        ("数える", "かぞえる", "to count", ["スウ", "ス"], ["かぞ.える", "かず"]),
        ("数学", "すうがく", "mathematics", ["スウガク"], []),
        ("数", "かず", "number / amount", ["スウ"], ["かず"]),
    ],
    # Lesson 43[cite: 19]
    [
        ("数日", "すうじつ", "a few days", ["スウジツ"], []),
        ("数年", "すうねん", "a few years", ["スウネン"], []),
        ("少数", "しょうすう", "minority / small number", ["ショウスウ"], []),
        ("数か月", "すうかげつ", "several months", ["スウカゲツ"], []),
        ("人数", "にんずう", "number of people", ["ニンズウ"], []),
    ],
    # Lesson 44[cite: 19]
    [
        ("美しい", "うつくしい", "beautiful / lovely", ["ビ"], ["うつく.しい"]),
        ("回す", "まわす", "to turn / rotate", ["カイ", "エ"], ["まわ.す", "まわ.る"]),
        ("数回", "すうかい", "several times", ["スウカイ"], []),
        ("回", "かい", "times / counter", ["カイ"], []),
        ("美味しい", "おいしい", "delicious / tasty", ["ビミ"], ["おい.しい"]),
    ],
    # Lesson 45[cite: 19]
    [
        ("何回", "なんかい", "how many times", ["ナンカイ"], []),
        ("回答", "かいとう", "reply / answer", ["カイトウ"], []),
        ("何回も", "なんかいも", "many times / repeatedly", ["ナンカイ"], []),
        ("回り道", "まわりみち", "detour", [], ["まわりみち"]),
        ("鳥取", "とっとり", "Tottori Prefecture", [], ["とっとり"]),
    ],
    # Lesson 46[cite: 19]
    [
        ("表", "おもて", "surface / front / table", ["ヒョウ"], ["おもて", "あらわ.す"]),
        ("表す", "あらわす", "to express / show", ["ヒョウ"], ["あらわ.す"]),
        ("表れる", "あらわれる", "to appear / be expressed", ["ヒョウ"], ["あらわ.れる"]),
        ("表情", "ひょうじょう", "facial expression", ["ヒョウジョウ"], []),
        ("手品", "てじな", "magic trick", [], ["てじな"]),
    ],
    # Lesson 47[cite: 19]
    [
        ("表面", "ひょうめん", "surface / exterior", ["ヒョウメン"], []),
        ("発表", "はっぴょう", "announcement / presentation", ["ハッピョウ"], []),
        ("表現", "ひょうげん", "expression / representation", ["ヒョウゲン"], []),
        ("無表情", "むひょうじょう", "expressionless", ["ムヒョウジョウ"], []),
        ("上手い", "うまい", "skillful / delicious", ["ジョウズ"], ["うま.い"]),
    ],
    # Lesson 48[cite: 19]
    [
        ("声", "こえ", "voice", ["セイ", "ショウ"], ["こえ", "こわ-"]),
        ("大声", "おおごえ", "loud voice", ["タイセイ"], ["おおごえ"]),
        ("報じる", "ほうじる", "to report / inform", ["ホウ"], ["むく.いる"]),
        ("情報", "じょうほう", "information / news", ["ジョウホウ"], []),
        ("音声", "おんせい", "voice / audio / speech", ["オンセイ"], []),
    ],
    # Lesson 49[cite: 19]
    [
        ("要するに", "ようするに", "in short / to sum up", ["ヨウ"], ["い.る"]),
        ("重要", "じゅうよう", "important / essential", ["ジュウヨウ"], []),
        ("変", "へん", "strange / weird / change", ["ヘン"], ["か.わる", "か.える"]),
        ("変わる", "かわる", "to change (intransitive)", ["ヘン"], ["か.わる"]),
        ("要る", "いる", "to need / require", ["ヨウ"], ["い.る"]),
    ],
    # Lesson 50[cite: 19]
    [
        ("変える", "かえる", "to change (transitive)", ["ヘン"], ["か.える"]),
        ("大変", "たいへん", "very / difficult / serious", ["タイヘン"], []),
        ("変化", "へんか", "change / variation", ["ヘンカ"], []),
        ("相変わらず", "あいかわらず", "as usual / as ever", [], ["あいかわらず"]),
        ("電報", "でんぽう", "telegram", ["デンポウ"], []),
    ],
    # Lesson 51[cite: 20]
    [
        ("お礼", "おれい", "thanks / gratitude / bow", ["レイ"], []),
        ("神", "かみ", "god / deity / spirit", ["シン", "ジン"], ["かみ", "かん"]),
        ("神社", "じんじゃ", "Shinto shrine", ["ジンジャ"], []),
        ("記", "き", "account / chronicle", ["キ"], ["しる.す"]),
        ("女神", "めがみ", "goddess", ["ジョシン"], ["めがみ"]),
    ],
    # Lesson 52[cite: 20]
    [
        ("記事", "きじ", "article / news story", ["キジ"], []),
        ("日記", "にっき", "diary / journal", ["ニッキ"], []),
        ("記入", "きにゅう", "entry / filling in", ["キニュウ"], []),
        ("和", "わ", "harmony / peace / Japanese", ["ワ", "オ"], ["やわ.らぐ"]),
    ],
    # Lesson 53[cite: 20]
    [
        ("和食", "わしょく", "Japanese food", ["ワショク"], []),
        ("和室", "わしつ", "Japanese-style room", ["ワシツ"], []),
        ("平和", "へいわ", "peace / harmony", ["ヘイワ"], []),
        ("引く", "ひく", "to pull / draw", ["イン"], ["ひ.く", "ひ.ける"]),
        ("取引", "とりひき", "transaction / business deal", [], ["とりひき"]),
    ],
    # Lesson 54[cite: 20]
    [
        ("引き出し", "ひきだし", "drawer", [], ["ひきだし"]),
        ("引き分け", "ひきわけ", "draw / tie game", [], ["ひきわけ"]),
        ("引き出す", "ひきだす", "to pull out / withdraw", [], ["ひきだ.す"]),
        ("治る", "なおる", "to be cured / heal", ["ジ", "チ"], ["なお.る", "おさ.める"]),
    ],
    # Lesson 55[cite: 20]
    [
        ("治す", "なおす", "to cure / heal", ["ジ", "チ"], ["なお.す"]),
        ("政治", "せいじ", "politics / government", ["セイジ"], []),
        ("政治家", "せいじか", "politician", ["セイジカ"], []),
        ("決して", "けっして", "never / by no means", ["ケッ"], ["けっ.して"]),
    ],
    # Lesson 56[cite: 20]
    [
        ("決まる", "きまる", "to be decided", ["ケツ"], ["き.まる"]),
        ("決める", "きめる", "to decide", ["ケツ"], ["き.める"]),
        ("太い", "ふとい", "thick / fat", ["タイ", "タ"], ["ふと.い", "ふと.る"]),
        ("太る", "ふとる", "to gain weight / grow fat", ["タイ"], ["ふと.る"]),
    ],
    # Lesson 57[cite: 20]
    [
        ("太め", "ふとめ", "on the plump/thick side", ["タイ"], ["ふと.め"]),
        ("受かる", "うかる", "to pass (an exam)", ["ジュ"], ["う.かる"]),
        ("受ける", "うける", "to receive / take (an exam)", ["ジュ"], ["う.ける"]),
        ("受信", "じゅしん", "receiving (a message/signal)", ["ジュシン"], []),
    ],
    # Lesson 58[cite: 20]
    [
        ("受け取る", "うけとる", "to receive / accept", [], ["うけと.る"]),
        ("受信者", "じゅしんしゃ", "recipient / receiver", ["ジュシンシャ"], []),
        ("解く", "とく", "to untie / solve", ["カイ", "ゲ"], ["と.く", "と.ける"]),
        ("正解", "せいかい", "correct answer", ["セイカイ"], []),
    ],
    # Lesson 59[cite: 20]
    [
        ("理解", "りかい", "understanding / comprehension", ["リカイ"], []),
        ("市", "し", "city", ["シ"], ["いち"]),
        ("市", "いち", "market / fair", ["シ"], ["いち"]),
        ("市立", "しりつ", "municipal / city-run", ["シリツ"], []),
    ],
    # Lesson 60[cite: 20]
    [
        ("市民", "しみん", "citizen", ["シミン"], []),
        ("期", "き", "period / term", ["キ", "ゴ"], []),
        ("学期", "がっき", "school term / semester", ["ガッキ"], []),
        ("期間", "きかん", "period / interval", ["キカン"], []),
        ("画期的", "かっきてき", "groundbreaking / epoch-making", ["カッキテキ"], []),
    ],
    # Lesson 61[cite: 20]
    [
        ("前期", "ぜんき", "first half / first term", ["ゼンキ"], []),
        ("後期", "こうき", "second half / latter term", ["コウキ"], []),
        ("同期", "どうき", "same period / contemporary", ["ドウキ"], []),
        ("長期", "ちょうき", "long term", ["チョウキ"], []),
    ],
    # Lesson 62[cite: 20]
    [
        ("期待", "きたい", "expectation / anticipation", ["キタイ"], []),
        ("様", "さま", "Mr. / Ms. / appearance", ["ヨウ"], ["さま"]),
        ("様子", "ようす", "state / appearance / situation", ["ヨウス"], []),
        ("活", "かつ", "living / active", ["カツ"], []),
        ("活性", "かっせい", "activity / vitality", ["カッセイ"], []),
    ],
    # Lesson 63[cite: 20]
    [
        ("生活", "せいかつ", "life / living", ["セイカツ"], []),
        ("活動", "かつどう", "activity / action", ["カツドウ"], []),
        ("頭", "あたま", "head / mind", ["トウ", "ズ", "ト"], ["あたま", "かしら"]),
        ("頭にくる", "あたまにくる", "to get angry / annoyed", [], ["あたまにくる"]),
    ],
    # Lesson 64[cite: 20]
    [
        ("頭がいい", "あたまがいい", "smart / clever", [], ["あたまがいい"]),
        ("組", "くみ", "class / group / team", ["ソ"], ["く.む", "くみ"]),
        ("組む", "くむ", "to put together / cross", ["ソ"], ["く.む"]),
        ("組み立てる", "くみたてる", "to assemble / construct", [], ["くみた.てる"]),
    ],
    # Lesson 65[cite: 20]
    [
        ("指", "ゆび", "finger / toe", ["シ"], ["ゆび", "さ.す"]),
        ("指定", "してい", "designation / specification", ["シテイ"], []),
        ("目指す", "めざす", "to aim at", [], ["めざ.す"]),
        ("指輪", "ゆびわ", "ring", [], ["ゆびわ"]),
        ("指す", "さす", "to point", ["シ"], ["さ.す"]),
    ],
    # Lesson 66[cite: 20]
    [
        ("小指", "こゆび", "little finger / pinky", [], ["こゆび"]),
        ("説明", "せつめい", "explanation", ["セツメイ"], []),
        ("能", "のう", "ability / Noh theater", ["ノウ"], []),
        ("能力", "のうりょく", "ability / capability", ["ノウリョク"], []),
        ("可能", "かのう", "possible / potential", ["カノウ"], []),
    ],
    # Lesson 67[cite: 20]
    [
        ("可能性", "かのうせい", "possibility", ["カノウセイ"], []),
        ("不可能", "ふかのう", "impossible", ["フカノウ"], []),
        ("葉", "は", "leaf", ["ヨウ"], ["は"]),
        ("言葉", "ことば", "word / language", [], ["ことば"]),
        ("葉書", "はがき", "postcard", ["ヨウショ"], ["はがき"]),
    ],
    # Lesson 68[cite: 20]
    [
        ("秋葉原", "あきはばら", "Akihabara", [], ["あきはばら"]),
        ("流れ", "ながれ", "flow / stream / current", ["リュウ"], ["なが.れ"]),
        ("流す", "ながす", "to pour / flush / shed", ["リュウ"], ["なが.す"]),
        ("流れる", "ながれる", "to flow / stream", ["リュウ"], ["なが.れる"]),
        ("千葉", "ちば", "Chiba Prefecture", [], ["ちば"]),
    ],
    # Lesson 69[cite: 20]
    [
        ("一流", "いちりゅう", "first-class / top-rate", ["イチリュウ"], []),
        ("流行", "りゅうこう", "fashion / trend", ["リュウコウ"], []),
        ("流し台", "ながしだい", "kitchen sink", [], ["ながしだい"]),
        ("流行り", "はやり", "trend / craze", [], ["はや.り"]),
    ],
    # Lesson 70[cite: 20]
    [
        ("流行る", "はやる", "to be popular / in fashion", ["リュウコウ"], ["はや.る"]),
        ("流行語", "りゅうこうご", "buzzword / trendy phrase", ["リュウコウゴ"], []),
        ("然", "ぜん", "so / thus / nature", ["ゼン", "ネン"], []),
        ("全然", "ぜんぜん", "not at all / completely", ["ゼンゼン"], []),
        ("天然", "てんねん", "nature / spontaneous", ["テンネン"], []),
    ],
    # Lesson 71[cite: 21]
    [
        ("当然", "とうぜん", "natural / of course", ["トウゼン"], []),
        ("不自然", "ふしぜん", "unnatural", ["フシゼン"], []),
        ("初め", "はじめ", "beginning / start", ["ショ"], ["はじ.め"]),
        ("初めて", "はじめて", "for the first time", ["ショ"], ["はじ.めて"]),
    ],
    # Lesson 72[cite: 21]
    [
        ("最初", "さいしょ", "first / beginning", ["サイショ"], []),
        ("在る", "ある", "to be / exist", ["ザイ"], ["あ.る"]),
        ("現在", "げんざい", "present time / now", ["ゲンザイ"], []),
        ("調べる", "しらべる", "to investigate / check", ["チョウ"], ["しら.べる"]),
        ("口調", "くちょう", "tone of voice", ["クチョウ"], []),
    ],
    # Lesson 73[cite: 21]
    [
        ("調子", "ちょうし", "condition / tone / rhythm", ["チョウシ"], []),
        ("調味料", "ちょうみりょう", "seasoning / condiment", ["チョウミリョウ"], []),
        ("議", "ぎ", "deliberation / discussion", ["ギ"], []),
        ("会議", "かいぎ", "meeting / conference", ["カイギ"], []),
    ],
    # Lesson 74[cite: 21]
    [
        ("会議室", "かいぎしつ", "conference room", ["カイギシツ"], []),
        ("不思議", "ふしぎ", "mysterious / wonderful", ["フシギ"], []),
        ("直す", "なおす", "to fix / repair / correct", ["チョク", "ジキ"], ["なお.す", "ただ.ちに"]),
        ("正直", "しょうじき", "honest / frank", ["ショウジキ"], []),
        ("直ちに", "ただちに", "immediately / at once", ["チョク"], ["ただ.ちに"]),
    ],
    # Lesson 75[cite: 21]
    [
        ("見直す", "みなおす", "to review / reconsider", [], ["みなお.す"]),
        ("言い直す", "いいなおす", "to rephrase / say again", [], ["いいなお.す"]),
        ("正直者", "しょうじきもの", "honest person", ["ショウジキモノ"], []),
        ("夫", "おっと", "husband", ["フ", "フウ"], ["おっと"]),
        ("直に", "じかに", "directly / in person", ["ジキ"], ["じか.に"]),
    ],
    # Lesson 76[cite: 21]
    [
        ("選ぶ", "えらぶ", "to choose / select", ["セン"], ["えら.ぶ"]),
        ("選手", "せんしゅ", "athlete / player", ["センシュ"], []),
        ("権", "けん", "authority / right", ["ケン", "ゴン"], []),
        ("利", "り", "profit / benefit / advantage", ["リ"], ["き.く"]),
    ],
    # Lesson 77[cite: 21]
    [
        ("利用", "りよう", "use / utilization", ["リヨウ"], []),
        ("利口", "りこう", "clever / smart", ["リコウ"], []),
        ("制", "せい", "system / control", ["セイ"], []),
        ("制作", "せいさく", "production / creation", ["セイサク"], []),
        ("制度", "せいど", "system / institution", ["セイド"], []),
    ],
    # Lesson 78[cite: 21]
    [
        ("続く", "つづく", "to continue (intransitive)", ["ゾク"], ["つづ.く"]),
        ("続ける", "つづける", "to continue (transitive)", ["ゾク"], ["つづ.ける"]),
        ("手続き", "てつづき", "procedure / formalities", [], ["てつづき"]),
        ("石", "いし", "stone / rock", ["セキ", "シャク"], ["いし"]),
        ("手続", "てつづき", "procedure / process", [], ["てつづき"]),
    ],
    # Lesson 79[cite: 21]
    [
        ("進む", "すすむ", "to advance / proceed", ["シン"], ["すす.む", "すす.める"]),
        ("進学", "しんがく", "advancing to higher education", ["シンガク"], []),
        ("進歩", "しんぽ", "progress / advancement", ["シンポ"], []),
        ("伝わる", "つたわる", "to be transmitted / handed down", ["デン"], ["つた.わる"]),
        ("流石", "さすが", "as expected / indeed", [], ["さすが"]),
    ],
    # Lesson 80[cite: 21]
    [
        ("伝える", "つたえる", "to convey / report", ["デン"], ["つた.える"]),
        ("手伝う", "てつだう", "to help / assist", [], ["てつだ.う"]),
        ("加える", "くわえる", "to add / include", ["カ"], ["くわ.える", "くわ.わる"]),
        ("助かる", "たすかる", "to be saved / helpful", ["ジョ"], ["たす.かる"]),
        ("連続", "れんぞく", "continuation / consecutive", ["レンゾク"], []),
    ],
    # Lesson 81[cite: 21]
    [
        ("助ける", "たすける", "to help / save / rescue", ["ジョ"], ["たす.ける"]),
        ("点", "てん", "point / dot / score", ["テン"], ["つ.ける"]),
        ("終点", "しゅうてん", "terminus / last stop", ["シュウテン"], []),
        ("欠点", "けってん", "flaw / weak point", ["ケッテン"], []),
        ("手助け", "てだすけ", "help / assistance", [], ["てだすけ"]),
    ],
    # Lesson 82[cite: 21]
    [
        ("産む", "うむ", "to give birth / produce", ["サン"], ["う.む", "う.まれる"]),
        ("産業", "さんぎょう", "industry", ["サンギョウ"], []),
        ("お土産", "おみやげ", "souvenir", [], ["おみやげ"]),
        ("務める", "つとめる", "to serve / work for", ["ム"], ["つと.める"]),
    ],
    # Lesson 83[cite: 21]
    [
        ("事務", "じむ", "office work / clerical work", ["ジム"], []),
        ("公務員", "こうむいん", "civil servant / government worker", ["コウムイン"], []),
        ("事務所", "じむしょ", "office", ["ジムショ"], []),
        ("件", "けん", "matter / case / item", ["ケン"], []),
        ("事件", "じけん", "incident / affair / case", ["ジケン"], []),
    ],
    # Lesson 84[cite: 21]
    [
        ("件名", "けんめい", "subject line / title", ["ケンメイ"], []),
        ("命", "いのち", "life / fate / command", ["メイ", "ミョウ"], ["いのち"]),
        ("番", "ばん", "number / turn / watch", ["バン"], []),
        ("何番", "なんばん", "what number", ["ナンバン"], []),
    ],
    # Lesson 85[cite: 21]
    [
        ("一番", "いちばん", "number one / best / most", ["イチバン"], []),
        ("二番", "にばん", "number two / second", ["ニバン"], []),
        ("三番", "さんばん", "number three / third", ["サンバン"], []),
        ("四番", "よんばん", "number four / fourth", ["ヨンバン"], []),
    ],
    # Lesson 86[cite: 21]
    [
        ("五番", "ごばん", "number five / fifth", ["ゴバン"], []),
        ("六番", "ろくばん", "number six / sixth", ["ロクバン"], []),
        ("七番", "ななばん", "number seven / seventh", ["ナナバン"], []),
        ("八番", "はちばん", "number eight / eighth", ["ハチバン"], []),
    ],
    # Lesson 87[cite: 22]
    [
        ("九番", "きゅうばん", "number nine / ninth", ["キュウバン"], []),
        ("十番", "じゅうばん", "number ten / tenth", ["ジュウバン"], []),
        ("番組", "ばんぐみ", "TV/radio program", ["バングミ"], []),
        ("落ちる", "おちる", "to fall / drop / fail", ["ラク"], ["お.ちる", "お.とす"]),
    ],
    # Lesson 88[cite: 22]
    [
        ("落とす", "おとす", "to drop / lose", ["ラク"], ["お.とす"]),
        ("落ち着く", "おちつく", "to calm down / settle down", [], ["おちつ.く"]),
        ("落ち込む", "おちこむ", "to feel down / depressed", [], ["おちこ.む"]),
        ("付く", "つく", "to be attached / adhere", ["フ"], ["つ.く", "つ.ける"]),
    ],
    # Lesson 89[cite: 22]
    [
        ("付ける", "つける", "to attach / put on", ["フ"], ["つ.ける"]),
        ("日付", "ひづけ", "date", [], ["ひづけ"]),
        ("受付", "うけつけ", "reception desk", [], ["うけつけ"]),
        ("気付く", "きづく", "to notice / realize", [], ["きづ.く"]),
    ],
    # Lesson 90[cite: 22]
    [
        ("付き合い", "つきあい", "association / socializing", [], ["つきあい"]),
        ("見付かる", "みつかる", "to be found", [], ["みつか.る"]),
        ("付き合う", "つきあう", "to associate with / date", [], ["つきあ.う"]),
        ("見付ける", "みつける", "to find / discover", [], ["みつけ.る"]),
    ],
    # Lesson 91[cite: 22]
    [
        ("気を付ける", "きをつける", "to be careful / pay attention", [], ["きをつけ.る"]),
        ("受け付ける", "うけつける", "to accept / receive", [], ["うけつけ.る"]),
        ("得", "とく", "profit / advantage", ["トク"], ["え.る", "う.る"]),
        ("得る", "える", "to obtain / gain", ["トク"], ["え.る"]),
    ],
    # Lesson 92[cite: 22]
    [
        ("得意", "とくい", "proud / strong point", ["トクイ"], []),
        ("好み", "このみ", "liking / taste / preference", ["コウ"], ["この.み"]),
        ("好む", "このむ", "to like / prefer", ["コウ"], ["この.む", "す.く"]),
        ("好き", "すき", "liked / favorite", ["コウ"], ["す.き"]),
        ("大好き", "だいすき", "love very much", ["ダイスキ"], []),
    ],
    # Lesson 93[cite: 22]
    [
        ("友好", "ゆうこう", "friendship", ["ユウコウ"], []),
        ("友好国", "ゆうこうこく", "friendly nation", ["ユウコウコク"], []),
        ("違う", "ちがう", "to differ / be wrong", ["イ"], ["ちが.う", "ちが.える"]),
        ("間違い", "まちがい", "mistake / error", [], ["まちがい"]),
    ],
    # Lesson 94[cite: 22]
    [
        ("間違う", "まちがう", "to make a mistake", [], ["まちが.う"]),
        ("間違える", "まちがえる", "to mistake / confuse", [], ["まちが.える"]),
        ("殺す", "ころす", "to kill", ["サツ", "サイ"], ["ころ.す"]),
        ("自殺", "じさつ", "suicide", ["ジサツ"], []),
    ],
    # Lesson 95[cite: 22]
    [
        ("置く", "おく", "to put / place", ["チ"], ["お.く"]),
        ("物置", "ものおき", "storeroom / shed", [], ["ものおき"]),
        ("返す", "かえす", "to return (something)", ["ヘン"], ["かえ.す", "かえ.る"]),
        ("ひっくり返る", "ひっくりかえる", "to overturn / tip over", [], ["ひっくりかえ.る"]),
    ],
    # Lesson 96[cite: 22]
    [
        ("ひっくり返す", "ひっくりかえす", "to turn over / knock over", [], ["ひっくりかえ.す"]),
        ("返事", "へんじ", "reply / answer", ["ヘンジ"], []),
        ("返信", "へんしん", "reply (message/email)", ["ヘンシン"], []),
        ("言い返す", "いいかえす", "to talk back / retort", [], ["いいかえ.す"]),
    ],
    # Lesson 97[cite: 22]
    [
        ("聞き返す", "ききかえす", "to ask back / ask again", [], ["ききかえ.す"]),
        ("論じる", "ろんじる", "to argue / discuss", ["ロン"], ["ろん.じる"]),
        ("論文", "ろんぶん", "thesis / essay / paper", ["ロンブン"], []),
        ("示す", "しめす", "to show / indicate", ["ジ", "シ"], ["しめ.す"]),
    ],
    # Lesson 98[cite: 22]
    [
        ("指示", "しじ", "instruction / direction", ["シジ"], []),
        ("際", "さい", "occasion / time / edge", ["サイ"], ["きわ"]),
        ("国際", "こくさい", "international", ["コクサイ"], []),
        ("国際化", "こくさいか", "internationalization", ["コクサイカ"], []),
    ],
    # Lesson 99[cite: 22]
    [
        ("歳", "さい", "years old / age", ["サイ", "セイ"], ["とし"]),
        ("何歳", "なんさい", "how old", ["ナンサイ"], []),
        ("反", "はん", "anti- / opposite", ["ハン", "ホン", "タン"], ["そ.る"]),
        ("反対", "はんたい", "opposition / opposite", ["ハンタイ"], []),
    ],
    # Lesson 100[cite: 22]
    [
        ("スピード違反", "スピードいはん", "speeding violation", ["イハン"], []),
        ("形", "かたち", "shape / form", ["ケイ", "ギョウ"], ["かた", "かたち"]),
        ("光る", "ひかる", "to shine / glitter", ["コウ"], ["ひか.る", "ひかり"]),
        ("日光", "にっこう", "sunlight / Nikko", ["ニッコウ"], []),
        ("光", "ひかり", "light", ["コウ"], ["ひかり"]),
    ],
    # Lesson 101[cite: 23]
    [
        ("首", "くび", "neck / head", ["シュ"], ["くび"]),
        ("首相", "しゅしょう", "Prime Minister", ["シュショウ"], []),
        ("勝つ", "かつ", "to win", ["ショウ"], ["か.つ", "まさ.る"]),
        ("勝手", "かって", "selfish / one's own way", ["カッテ"], []),
        ("人形", "にんぎょう", "doll / puppet", ["ニンギョウ"], []),
    ],
    # Lesson 102[cite: 23]
    [
        ("必ず", "かならず", "without fail / certainly", ["ヒツ"], ["かなら.ず"]),
        ("必要", "ひつよう", "necessary / essential", ["ヒツヨウ"], []),
        ("係", "かかり", "person in charge / duty", ["ケイ"], ["かか.る", "かかり"]),
        ("関係", "かんけい", "relationship / connection", ["カンケイ"], []),
        ("必死", "ひっし", "frantic / desperate", ["ヒッシ"], []),
    ],
    # Lesson 103[cite: 23]
    [
        ("友好関係", "ゆうこうかんけい", "friendly relations", ["ユウコウカンケイ"], []),
        ("由", "よし", "reason / significance", ["ユ", "ユウ", "ユイ"], ["よし"]),
        ("理由", "りゆう", "reason / cause", ["リユウ"], []),
        ("経由", "けいゆ", "via / by way of", ["ケイユ"], []),
        ("使い勝手", "つかいがって", "ease of use", [], ["つかいがって"]),
    ],
    # Lesson 104[cite: 23]
    [
        ("自由", "じゆう", "freedom / liberty", ["ジユウ"], []),
        ("自由化", "じゆうか", "liberalization", ["ジユウカ"], []),
        ("不自由", "ふじゆう", "inconvenience / disability", ["フジユウ"], []),
        ("愛する", "あいする", "to love", ["アイ"], ["あい.する"]),
        ("可愛い", "かわいい", "cute / adorable", [], ["かわい.い"]),
    ],
    # Lesson 105[cite: 23]
    [
        ("愛情", "あいじょう", "love / affection", ["アイジョウ"], []),
        ("可愛がる", "かわいがる", "to dote on / cherish", [], ["かわいが.る"]),
        ("老い", "おい", "old age", ["ロウ"], ["お.いる"]),
        ("老人", "ろうじん", "elderly person", ["ロウジン"], []),
    ],
    # Lesson 106[cite: 23]
    [
        ("老人ホーム", "ろうじんホーム", "nursing home", ["ロウジン"], []),
        ("都", "みやこ", "capital / metropolis", ["ト", "ツ"], ["みやこ"]),
        ("都", "と", "metropolis (Tokyo)", ["ト"], []),
        ("都会", "とかい", "city / urban area", ["トカイ"], []),
    ],
    # Lesson 107[cite: 23]
    [
        ("首都", "しゅと", "capital city", ["シュト"], []),
        ("京都", "きょうと", "Kyoto", ["キョウト"], []),
        ("都合", "つごう", "convenience / circumstances", ["ツゴウ"], []),
        ("都合がいい", "つごうがいい", "convenient", ["ツゴウ"], []),
    ],
    # Lesson 108[cite: 23]
    [
        ("都合が悪い", "つごうがわるい", "inconvenient", ["ツゴウ"], []),
        ("放す", "はなす", "to release / let go", ["ホウ"], ["はな.す", "はな.れる"]),
        ("放送", "ほうそう", "broadcasting", ["ホウソウ"], []),
        ("生放送", "なまほうそう", "live broadcast", ["ナマホウソウ"], []),
    ],
    # Lesson 109[cite: 23]
    [
        ("食べ放題", "たべほうだい", "all-you-can-eat", [], ["たべほうだい"]),
        ("飲み放題", "のみほうだい", "all-you-can-drink", [], ["のみほうだい"]),
        ("確か", "たしか", "certain / sure / if I remember", ["カク"], ["たし.か", "たし.かめる"]),
        ("確かに", "たしかに", "surely / certainly", ["カク"], ["たし.かに"]),
    ],
    # Lesson 110[cite: 23]
    [
        ("確かめる", "たしかめる", "to ascertain / confirm", ["カク"], ["たし.かめる"]),
        ("正確", "せいかく", "accurate / exact", ["セイカク"], []),
        ("過ぎる", "すぎる", "to pass / exceed / too much", ["カ"], ["す.ぎる", "す.ごす"]),
        ("過ごす", "すごす", "to spend (time)", ["カ"], ["す.ごす"]),
        ("過去", "かこ", "the past", ["カコ"], []),
    ],
    # Lesson 111[cite: 23]
    [
        ("通過", "つうか", "passing through", ["ツウカ"], []),
        ("通り過ぎる", "とおりすぎる", "to go past / pass by", [], ["とおりす.ぎる"]),
        ("的", "まと", "target / mark", ["テキ"], ["まと"]),
        ("状", "じょう", "letter / condition / form", ["ジョウ"], []),
    ],
    # Lesson 112[cite: 23]
    [
        ("年賀状", "ねんがじょう", "New Year's greeting card", ["ネンガジョウ"], []),
        ("想", "そう", "concept / thought / idea", ["ソウ", "ソ"], []),
        ("想像", "そうぞう", "imagination", ["ソウゾウ"], []),
        ("理想的", "りそうてき", "ideal", ["リソウテキ"], []),
    ],
    # Lesson 113[cite: 23]
    [
        ("官", "かん", "government / official", ["カン"], []),
        ("交わる", "まじわる", "to intersect / associate", ["コウ"], ["まじ.わる", "ま.じる"]),
        ("交番", "こうばん", "police box", ["コウバン"], []),
        ("交通", "こうつう", "traffic / transportation", ["コウツウ"], []),
        ("交代", "こうたい", "alternation / change / shift", ["コウタイ"], []),
    ],
    # Lesson 114[cite: 23]
    [
        ("交際", "こうさい", "company / friendship / dating", ["コウサイ"], []),
        ("突然", "とつぜん", "suddenly / abruptly", ["トツゼン"], []),
        ("配る", "くばる", "to distribute / deliver", ["ハイ"], ["くば.る"]),
        ("心配", "しんぱい", "worry / anxiety", ["シンパイ"], []),
    ],
    # Lesson 115[cite: 23]
    [
        ("若い", "わかい", "young", ["ジャク", "ニャク"], ["わか.い"]),
        ("興じる", "きょうじる", "to amuse oneself / enjoy", ["キョウ", "コウ"], ["おこ.る"]),
        ("資料", "しりょう", "materials / data", ["シリョウ"], []),
        ("常に", "つねに", "always / constantly", ["ジョウ"], ["つね.に"]),
        ("若年", "じゃくねん", "youth / young age", ["ジャクネン"], []),
    ],
    # Lesson 116[cite: 23]
    [
        ("日常", "にちじょう", "ordinary / everyday", ["ニチジョウ"], []),
        ("正常", "せいじょう", "normal / normality", ["セイジョウ"], []),
        ("日常会話", "にちじょうかいわ", "everyday conversation", ["ニチジョウカイワ"], []),
        ("日常生活", "にちじょうせいかつ", "daily life", ["ニチジョウセイカツ"], []),
    ],
    # Lesson 117[cite: 23]
    [
        ("果たして", "はたして", "as expected / really", ["カ"], ["は.たす", "は.てる"]),
        ("果物", "くだもの", "fruit", [], ["くだもの"]),
        ("呼び", "よび", "call / invitation", ["コ"], ["よ.び"]),
        ("共に", "ともに", "together / both", ["キョウ"], ["とも.に"]),
        ("呼ぶ", "よぶ", "to call / invite", ["コ"], ["よ.ぶ"]),
    ],
    # Lesson 118[cite: 23]
    [
        ("公共料金", "こうきょうりょうきん", "public utility charges", ["コウキョウリョウキン"], []),
        ("残る", "のこる", "to remain / be left", ["ザン"], ["のこ.る", "のこ.す"]),
        ("残す", "のこす", "to leave behind / save", ["ザン"], ["のこ.す"]),
    ],
    # Lesson 119[cite: 23]
    [
        ("残業", "ざんぎょう", "overtime work", ["ザンギョウ"], []),
        ("残り物", "のこりもの", "leftovers", [], ["のこりもの"]),
        ("判", "はん", "seal / stamp / judgment", ["ハン", "バン"], []),
        ("判子", "はんこ", "personal seal / stamp", ["ハンコ"], []),
    ],
    # Lesson 120[cite: 23]
    [
        ("役", "やく", "role / duty / service", ["ヤク", "エキ"], []),
        ("市役所", "しやくしょ", "city hall / municipal office", ["シヤクショ"], []),
        ("続", "ぞく", "continuation / sequel", ["ゾク"], ["つづ.く"]),
        ("役人", "やくにん", "government official", ["ヤクニン"], []),
        ("現役", "げんえき", "active duty / active service", ["ゲンエキ"], []),
    ],
    # Lesson 121[cite: 23]
    [
        ("術", "じゅつ", "art / technique / skill", ["ジュツ"], []),
        ("美術", "びじゅつ", "fine arts", ["ビジュツ"], []),
        ("手術", "しゅじゅつ", "surgical operation", ["シュジュツ"], []),
        ("美術館", "びじゅつかん", "art museum", ["ビジュツカン"], []),
    ],
    # Lesson 122[cite: 23]
    [
        ("支える", "ささえる", "to support / sustain", ["シ"], ["ささ.える"]),
        ("支援", "しえん", "support / aid", ["シエン"], []),
        ("均", "きん", "level / average / equal", ["キン"], []),
        ("四角", "しかく", "square", ["シカク"], []),
    ],
    # Lesson 123[cite: 23]
    [
        ("曲線", "きょくせん", "curved line / curve", ["キョクセン"], []),
        ("乗る", "のる", "to ride / get on", ["ジョウ"], ["の.る", "の.せる"]),
        ("乗せる", "のせる", "to give a ride / place on", ["ジョウ"], ["の.せる"]),
        ("乗車", "じょうしゃ", "boarding a train/bus", ["ジョウシャ"], []),
    ],
    # Lesson 124[cite: 23]
    [
        ("乗り場", "のりば", "bus/taxi stop / platform", [], ["のりば"]),
        ("乗り過ごす", "のりすごす", "to ride past one's stop", [], ["のりすご.す"]),
        ("乗車口", "じょうしゃぐち", "boarding entrance", ["ジョウシャグチ"], []),
        ("済む", "すむ", "to finish / end / be settled", ["サイ"], ["す.む", "す.ます"]),
    ],
    # Lesson 125[cite: 23]
    [
        ("済ます", "すます", "to finish / get it over with", ["サイ"], ["す.ます"]),
        ("済ませる", "すませる", "to finish / complete", ["サイ"], ["す.ませる"]),
        ("経済", "けいざい", "economy / economics", ["ケイザイ"], []),
        ("公用", "こうよう", "official business", ["コウヨウ"], []),
    ],
    # Lesson 126[cite: 24]
    [
        ("子供", "こども", "child / children", ["コドモ"], []),
        ("格", "かく", "status / rank / case", ["カク", "コウ"], []),
        ("資格", "しかく", "qualification / license", ["シカク"], []),
        ("合格", "ごうかく", "passing an exam", ["ゴウカク"], []),
        ("格好", "かっこう", "appearance / shape / posture", ["カッコウ"], []),
    ],
    # Lesson 127[cite: 24]
    [
        ("不合格", "ふごうかく", "failure (in an exam)", ["フゴウカク"], []),
        ("打つ", "うつ", "to hit / strike / type", ["ダ"], ["う.つ"]),
        ("師", "し", "expert / teacher / master", ["シ"], []),
        ("新幹線", "しんかんせん", "Shinkansen (bullet train)", ["シンカンセン"], []),
        ("制御", "せいぎょ", "control / regulation", ["セイギョ"], []),
    ],
    # Lesson 128[cite: 24]
    [
        ("断る", "ことわる", "to refuse / decline", ["ダン"], ["ことわ.る", "た.つ"]),
        ("無断", "むだん", "without permission", ["ムダン"], []),
        ("断水", "だんすい", "water outage", ["ダンスイ"], []),
        ("式", "しき", "ceremony / formula / style", ["シキ"], []),
    ],
    # Lesson 129[cite: 24]
    [
        ("入学式", "にゅうがくしき", "entrance ceremony", ["ニュウガクシキ"], []),
        ("成人式", "せいじんしき", "coming-of-age ceremony", ["セイジンシキ"], []),
        ("的", "てき", "-like / -al (suffix)", ["テキ"], []),
        ("教師", "きょうし", "teacher / instructor", ["キョウシ"], []),
    ],
    # Lesson 130[cite: 24]
    [
        ("医師", "いし", "doctor / physician", ["イシ"], []),
        ("告げる", "つげる", "to tell / announce", ["コク"], ["つ.げる"]),
        ("報告", "ほうこく", "report / information", ["ホウコク"], []),
        ("広告", "こうこく", "advertisement", ["コウコク"], []),
    ],
    # Lesson 131[cite: 24]
    [
        ("広告会社", "こうこくがいしゃ", "advertising agency", ["コウコクガイシャ"], []),
        ("深い", "ふかい", "deep / profound", ["シン"], ["ふか.い", "ふか.まる"]),
        ("深夜", "しんや", "late at night", ["シンヤ"], []),
        ("深夜番組", "しんやばんぐみ", "late-night TV show", ["シンヤバングミ"], []),
    ],
    # Lesson 132[cite: 24]
    [
        ("ご存じ", "ごぞんじ", "knowing (honorific)", ["ゾン", "ソン"], []),
        ("存在", "そんざい", "existence / being", ["ソンザイ"], []),
        ("争い", "あらそい", "dispute / quarrel / conflict", ["ソウ"], ["あらそ.い"]),
        ("争う", "あらそう", "to compete / dispute", ["ソウ"], ["あらそ.う"]),
        ("ご存知", "ごぞんじ", "knowing (honorific)", ["ゾンチ"], []),
    ],
    # Lesson 133[cite: 24]
    [
        ("戦争", "せんそう", "war", ["センソウ"], []),
        ("言い争い", "いいあらそい", "quarrel / argument", [], ["いいあらそい"]),
        ("覚める", "さめる", "to wake up / become sober", ["カク"], ["さ.める", "さ.ます"]),
        ("覚える", "おぼえる", "to memorize / remember", ["カク"], ["おぼ.える"]),
    ],
    # Lesson 134[cite: 24]
    [
        ("覚ます", "さます", "to awaken / wake up", ["カク"], ["さ.ます"]),
        ("側", "がわ", "side / row", ["ソク"], ["がわ"]),
        ("右側", "みぎがわ", "right side", [], ["みぎがわ"]),
        ("内緒", "ないしょ", "secret / privacy", ["ナイショ"], []),
    ],
    # Lesson 135[cite: 24]
    [
        ("外側", "そとがわ", "outside / exterior", [], ["そとがわ"]),
        ("飛ぶ", "とぶ", "to fly / jump", ["ヒ"], ["と.ぶ", "と.ばす"]),
        ("飛ばす", "とばす", "to let fly / skip", ["ヒ"], ["と.ばす"]),
        ("飛び込む", "とびこむ", "to jump into / dive in", [], ["とびこ.む"]),
    ],
    # Lesson 136[cite: 24]
    [
        ("飛び出す", "とびだす", "to jump out / rush out", [], ["とびだ.す"]),
        ("飛行機", "ひこうき", "airplane", ["ヒコウキ"], []),
        ("参る", "まいる", "to go / come (humble)", ["サン"], ["まい.る"]),
        ("参加", "さんか", "participation", ["サンカ"], []),
        ("参考", "さんこう", "reference / consultation", ["サンコウ"], []),
    ],
    # Lesson 137[cite: 24]
    [
        ("突く", "つく", "to thrust / poke / stab", ["トツ"], ["つ.く"]),
        ("突然", "とつぜん", "suddenly", ["トツゼン"], []),
        ("突き当たり", "つきあたり", "end of a street / dead end", [], ["つきあたり"]),
        ("容", "よう", "form / appearance / contain", ["ヨウ"], []),
    ],
    # Lesson 138[cite: 24]
    [
        ("内容", "ないよう", "contents / subject matter", ["ナイヨウ"], []),
        ("美容院", "びよういん", "beauty parlor / hair salon", ["ビヨウイン"], []),
        ("美容師", "びようし", "beautician / hairdresser", ["ビヨウシ"], []),
        ("育てる", "そだてる", "to raise / bring up", ["イク"], ["そだ.てる", "そだ.つ"]),
    ],
    # Lesson 139[cite: 24]
    [
        ("育つ", "そだつ", "to grow up / be raised", ["イク"], ["そだ.つ"]),
        ("体育", "たいいく", "physical education", ["タイイク"], []),
        ("教育", "きょういく", "education", ["キョウイク"], []),
        ("体育館", "たいいくかん", "gymnasium", ["タイイクカン"], []),
    ],
    # Lesson 140[cite: 24]
    [
        ("構う", "かまう", "to mind / care about", ["コウ"], ["かま.う", "かま.える"]),
        ("構成", "こうせい", "composition / structure", ["コウセイ"], []),
        ("認める", "みとめる", "to recognize / admit", ["ニン"], ["みと.める"]),
        ("確認", "かくにん", "confirmation / verification", ["カクニン"], []),
    ],
    # Lesson 141[cite: 24]
    [
        ("位", "くらい", "rank / position / about", ["イ"], ["くらい"]),
        ("位置", "いち", "position / location", ["イチ"], []),
        ("順位", "じゅんい", "order / rank / standing", ["ジュンイ"], []),
        ("達する", "たっする", "to reach / attain", ["タツ"], ["たっ.する"]),
        ("友達", "ともだち", "friend", ["トモダチ"], []),
    ],
    # Lesson 142[cite: 24]
    [
        ("上達", "じょうたつ", "improvement / progress", ["ジョウタツ"], []),
        ("守る", "まもる", "to protect / obey", ["シュ", "ス"], ["まも.る", "もり"]),
        ("落ちる", "おちる", "to fall / drop", ["ラク"], ["お.ちる"]),
        ("遅刻", "ちこく", "lateness / tardiness", ["チコク"], []),
        ("満足", "まんぞく", "satisfaction", ["マンゾク"], []),
    ],
    # Lesson 143[cite: 24]
    [
        ("満車", "まんしゃ", "full (parking)", ["マンシャ"], []),
        ("不満", "ふまん", "dissatisfaction", ["フマン"], []),
        ("消す", "けす", "to erase / turn off", ["ショウ"], ["け.す", "き.える"]),
        ("消える", "きえる", "to disappear / go out", ["ショウ"], ["き.える"]),
    ],
    # Lesson 144[cite: 24]
    [
        ("消しゴム", "けしゴム", "eraser", [], ["けしゴム"]),
        ("解消", "かいしょう", "cancellation / relief (stress)", ["カイショウ"], []),
        ("取り消し", "とりけし", "cancellation / revocation", [], ["とりけし"]),
        ("取り消す", "とりけす", "to cancel / withdraw", [], ["とりけ.す"]),
    ],
    # Lesson 145[cite: 24]
    [
        ("任せる", "まかせる", "to entrust / leave to", ["ニン"], ["まか.せる"]),
        ("居る", "いる", "to be / exist (animate)", ["キョ"], ["い.る"]),
        ("居間", "いま", "living room", ["キョカン"], ["いま"]),
        ("居酒屋", "いざかや", "Japanese pub", ["イザカヤ"], []),
        ("居心地", "いごこち", "comfort / coziness", [], ["いごこち"]),
    ],
    # Lesson 146[cite: 24]
    [
        ("予め", "あらかじめ", "beforehand / in advance", ["ヨ"], ["あらかじ.め"]),
        ("予約", "よやく", "reservation / appointment", ["ヨヤク"], []),
        ("予習", "よしゅう", "preparation for a lesson", ["ヨシュウ"], []),
        ("予定", "よてい", "plan / schedule", ["ヨテイ"], []),
    ],
    # Lesson 147[cite: 24]
    [
        ("予想", "よそう", "expectation / prediction", ["ヨソウ"], []),
        ("予報", "よほう", "forecast / prediction", ["ヨホウ"], []),
        ("天気予報", "てんきよほう", "weather forecast", ["テンキヨホウ"], []),
        ("路", "みち", "road / path", ["ロ"], ["みち"]),
    ],
    # Lesson 148[cite: 24]
    [
        ("道路", "どうろ", "road / highway", ["ドウロ"], []),
        ("進路", "しんろ", "course / career path", ["シンロ"], []),
        ("線路", "せんろ", "railway track", ["センロ"], []),
        ("通路", "つうろ", "passage / aisle", ["ツウロ"], []),
    ],
    # Lesson 149[cite: 24]
    [
        ("座る", "すわる", "to sit", ["ザ"], ["すわ.る"]),
        ("口座", "こうざ", "bank account", ["コウザ"], []),
        ("銀座", "ぎんざ", "Ginza", ["ギンザ"], []),
        ("銀行口座", "ぎんこうこうざ", "bank account", ["ギンコウコウザ"], []),
    ],
    # Lesson 150[cite: 24]
    [
        ("お客さん", "おきゃくさん", "guest / customer", ["キャク"], []),
        ("乗客", "じょうきゃく", "passenger", ["ジョウキャク"], []),
        ("姫", "ひめ", "princess", [], ["ひめ"]),
        ("起因", "きいん", "cause / origin", ["キイン"], []),
    ],
    # Lesson 151[cite: 25]
    [
        ("追う", "おう", "to chase / pursue", ["ツイ"], ["お.う"]),
        ("追いつく", "おいつく", "to catch up with", [], ["おいつ.く"]),
        ("追いかける", "おいかける", "to chase after", [], ["おいかけ.る"]),
        ("追加", "ついか", "addition / supplement", ["ツイカ"], []),
    ],
    # Lesson 152[cite: 25]
    [
        ("背", "せ", "back / height / stature", ["ハイ"], ["せ", "せい", "そむ.く"]),
        ("背中", "せなか", "back (of body)", [], ["せなか"]),
        ("観", "かん", "view / appearance", ["カン"], []),
        ("観光", "かんこう", "sightseeing", ["カンコウ"], []),
        ("背広", "せびろ", "business suit", [], ["せびろ"]),
    ],
    # Lesson 153[cite: 25]
    [
        ("観光スポット", "かんこうスポット", "sightseeing spot", ["カンコウ"], []),
        ("観光地", "かんこうち", "tourist destination", ["カンコウチ"], []),
        ("観光客", "かんこうきゃく", "tourist", ["カンコウキャク"], []),
        ("誰", "だれ", "who", ["スイ"], ["だれ"]),
        ("眠る", "ねむる", "to sleep", ["ミン"], ["ねむ.る", "ねむ.い"]),
    ],
    # Lesson 154[cite: 25]
    [
        ("息", "いき", "breath / respiration", ["ソク"], ["いき"]),
        ("ため息", "ためいき", "sigh", [], ["ためいき"]),
        ("息子", "むすこ", "son", [], ["むすこ"]),
        ("一人息子", "ひとりむすこ", "only son", [], ["ひとりむすこ"]),
    ],
    # Lesson 155[cite: 25]
    [
        ("失う", "うしなう", "to lose / part with", ["シツ"], ["うしな.う"]),
        ("失敗", "しっぱい", "failure / mistake", ["シッパイ"], []),
        ("良い", "よい", "good / fine", ["リョウ"], ["よ.い", "い.い"]),
        ("最良", "さいりょう", "the best / ideal", ["サイリョウ"], []),
    ],
    # Lesson 156[cite: 25]
    [
        ("号", "ごう", "number / issue / edition", ["ゴウ"], []),
        ("信号", "しんごう", "traffic light / signal", ["シンゴウ"], []),
        ("論", "ろん", "argument / theory", ["ロン"], []),
        ("無論", "むろん", "of course / naturally", ["ムロン"], []),
        ("番号", "ばんごう", "number", ["バンゴウ"], []),
    ],
    # Lesson 157[cite: 25]
    [
        ("職業", "しょくぎょう", "occupation / profession", ["ショクギョウ"], []),
        ("識", "しき", "discernment / knowledge", ["シキ"], []),
        ("知識", "ちしき", "knowledge", ["チシキ"], []),
        ("常識的", "じょうしきてき", "common-sense / sensible", ["ジョウシキテキ"], []),
    ],
    # Lesson 158[cite: 25]
    [
        ("警", "けい", "admonish / guard / warn", ["ケイ"], []),
        ("警告", "けいこく", "warning / caution", ["ケイコク"], []),
        ("警官", "けいかん", "police officer", ["ケイカン"], []),
        ("優しい", "やさしい", "kind / gentle / easy", ["ユウ"], ["やさ.しい", "すぐ.れる"]),
    ],
    # Lesson 159[cite: 25]
    [
        ("優れる", "すぐれる", "to surpass / excel", ["ユウ"], ["すぐ.れる"]),
        ("優勝", "ゆうしょう", "overall victory / championship", ["ユウショウ"], []),
        ("投げる", "なげる", "to throw / pitch", ["トウ"], ["な.げる"]),
        ("テレビ局", "テレビきょく", "TV station", ["キョク"], []),
    ],
    # Lesson 160[cite: 25]
    [
        ("難しい", "むずかしい", "difficult / hard", ["ナン"], ["むずか.しい", "かた.い"]),
        ("難", "なん", "difficulty / trouble", ["ナン"], []),
        ("念", "ねん", "sense / idea / thought", ["ネン"], []),
        ("記念", "きねん", "commemoration / memory", ["キネン"], []),
    ],
    # Lesson 161[cite: 25]
    [
        ("記念日", "きねんび", "anniversary / memorial day", ["キネンビ"], []),
        ("寄る", "よる", "to approach / drop by", ["キ"], ["よ.る", "よ.せる"]),
        ("年寄り", "としより", "old person / elderly", [], ["としより"]),
        ("お年寄り", "おとしより", "elderly person (polite)", [], ["おとしより"]),
    ],
    # Lesson 162[cite: 25]
    [
        ("商", "しょう", "trade / merchant", ["ショウ"], ["あきな.う"]),
        ("商品", "しょうひん", "commodity / merchandise", ["ショウヒン"], []),
        ("商業", "しょうぎょう", "commerce / trade", ["ショウギョウ"], []),
        ("商売", "しょうばい", "trade / business", ["ショウバイ"], []),
    ],
    # Lesson 163[cite: 25]
    [
        ("害", "がい", "harm / injury / damage", ["ガイ"], []),
        ("加害者", "かがいしゃ", "assailant / perpetrator", ["カガイシャ"], []),
        ("頼む", "たのむ", "to request / ask / rely on", ["ライ"], ["たの.む", "たよ.る"]),
        ("晴", "はれ", "clear weather", ["セイ"], ["は.れる"]),
        ("頼る", "たよる", "to rely on / depend on", ["ライ"], ["たよ.る"]),
    ],
    # Lesson 164[cite: 25]
    [
        ("横書き", "よこがき", "horizontal writing", [], ["よこがき"]),
        ("横切る", "よこぎる", "to cross / traverse", [], ["よこぎ.る"]),
        ("増える", "ふえる", "to increase (intransitive)", ["ゾウ"], ["ふ.える", "ふ.やす"]),
        ("増やす", "ふやす", "to increase (transitive)", ["ゾウ"], ["ふ.やす"]),
        ("増す", "ます", "to increase / grow", ["ゾウ"], ["ま.す"]),
    ],
    # Lesson 165[cite: 25]
    [
        ("増加", "ぞうか", "increase / growth", ["ゾウカ"], []),
        ("差す", "さす", "to shine / hold up (umbrella)", ["サ"], ["さ.す"]),
        ("時差", "じさ", "time difference", ["ジサ"], []),
        ("差別", "さべつ", "discrimination / distinction", ["サベツ"], []),
        ("横断", "おうだん", "crossing", ["オウダン"], []),
    ],
    # Lesson 166[cite: 25]
    [
        ("時差ぼけ", "じさぼけ", "jet lag", ["ジサ"], []),
        ("差し上げる", "さしあげる", "to give / offer (humble)", [], ["さしあ.げる"]),
        ("差出人", "さしだしにん", "sender", [], ["さしだしにん"]),
        ("交差点", "こうさてん", "intersection", ["コウサテン"], []),
    ],
    # Lesson 167[cite: 25]
    [
        ("苦い", "にがい", "bitter", ["ク"], ["にが.い", "くる.しい"]),
        ("苦しむ", "くるしむ", "to suffer / groan", ["ク"], ["くる.しむ"]),
        ("苦情", "くじょう", "complaint / grievance", ["クジョウ"], []),
        ("苦手", "にがて", "poor at / weak in", ["ニガテ"], []),
        ("苦笑", "くしょう", "bitter smile / wry smile", ["クショウ"], []),
    ],
    # Lesson 168[cite: 25]
    [
        ("収める", "おさめる", "to obtain / reap / pay", ["シュウ"], ["おさ.める", "おさ.まる"]),
        ("収入", "しゅうにゅう", "income / revenue", ["シュウニュウ"], []),
        ("法", "のり", "rule / law", ["ホウ"], ["のり"]),
        ("手段", "しゅだん", "means / way / measure", ["シュダン"], []),
    ],
    # Lesson 169[cite: 25]
    [
        ("俺", "おれ", "I / me (masculine casual)", [], ["おれ"]),
        ("渡る", "わたる", "to cross over / go across", ["ト"], ["わた.る", "わた.す"]),
        ("渡す", "わたす", "to hand over / pass", ["ト"], ["わた.す"]),
        ("与える", "あたえる", "to give / bestow", ["ヨ"], ["あた.える"]),
    ],
    # Lesson 170[cite: 25]
    [
        ("演じる", "えんじる", "to perform / play a role", ["エン"], ["えん.じる"]),
        ("演技", "えんぎ", "acting / performance", ["エンギ"], []),
        ("備える", "そなえる", "to prepare / equip", ["ビ"], ["そな.える"]),
        ("申す", "もうす", "to say / be called (humble)", ["シン"], ["もう.す"]),
        ("申込", "もうしこみ", "application / subscription", [], ["もうしこみ"]),
    ],
    # Lesson 171[cite: 25]
    [
        ("申し込む", "もうしこむ", "to apply for / propose", [], ["もうしこ.む"]),
        ("例えば", "たとえば", "for example", ["レイ"], ["たと.えば"]),
        ("働く", "はたらく", "to work", ["ドウ"], ["はたら.く"]),
        ("働き者", "はたらきもの", "hard worker", [], ["はたらきもの"]),
    ],
    # Lesson 172[cite: 25]
    [
        ("景", "けい", "scenery / view", ["ケイ"], []),
        ("景色", "けしき", "scenery / landscape", ["ケシキ"], []),
        ("不景気", "ふけいき", "economic recession / slump", ["フケイキ"], []),
        ("抜く", "ぬく", "to pull out / extract", ["バツ"], ["ぬ.く", "ぬ.ける"]),
        ("見本", "みほん", "sample / specimen", [], ["みほん"]),
    ],
    # Lesson 173[cite: 25]
    [
        ("抜ける", "ぬける", "to come out / fall out", ["バツ"], ["ぬ.ける"]),
        ("遠く", "とおく", "far away / distance", ["エン"], ["とお.く"]),
        ("遠い", "とおい", "far / distant", ["エン", "オン"], ["とお.い"]),
        ("遠回り", "とおまわり", "detour", [], ["とおまわり"]),
    ],
    # Lesson 174[cite: 27]
    [
        ("絶えず", "たえず", "constantly / ceaselessly", ["ゼツ"], ["た.えず"]),
        ("絶対", "ぜったい", "absolutely / unconditionally", ["ゼッタイ"], []),
        ("負ける", "まける", "to lose / be defeated", ["フ"], ["ま.ける", "お.う"]),
        ("福", "ふく", "blessing / fortune / luck", ["フク"], []),
        ("福音", "ふくいん", "gospel / good news", ["フクイン"], []),
    ],
    # Lesson 175[cite: 27]
    [
        ("球", "たま", "ball / sphere / globe", ["キュウ"], ["たま"]),
        ("球", "きゅう", "sphere / ball", ["キュウ"], ["たま"]),
        ("野球", "やきゅう", "baseball", ["ヤキュウ"], []),
        ("地球", "ちきゅう", "the Earth", ["チキュウ"], []),
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
    if not os.path.isdir(KANJIVG_DIR):
        raise FileNotFoundError(f"Could not find '{KANJIVG_DIR}'.")

    lessons = []
    item_counter = 1

    for l_idx, chunk in enumerate(N3_PART1_DATA):
        lesson_num = l_idx + 1
        lesson_items = []

        for word, kana, meaning, onyomi, kunyomi in chunk:
            characters_data = []
            for ch in word:
                characters_data.append({
                    "char": ch,
                    "strokes": get_strokes_for_char(ch),
                })

            lesson_items.append({
                "id": f"n3-{item_counter}",
                "level": "N3",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n3-lesson-{lesson_num}",
            "level": "N3",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    with open(PART1_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 1 complete! Saved Lessons 1-175 ({item_counter - 1} items) to {PART1_JSON_PATH}.")


if __name__ == "__main__":
    main()