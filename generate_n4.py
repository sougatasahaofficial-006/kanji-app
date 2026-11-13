import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
OUTPUT_TS_PATH = os.path.join("src", "data", "n4.ts")

# Complete 95-Lesson JLPT N4 Curriculum (4–5 items per lesson = 390 items total)
N4_LESSONS_DATA = [
    # Lesson 1[cite: 21]
    [
        ("明るい", "あかるい", "bright / cheerful", ["メイ", "ミョウ"], ["あか.るい", "あ.ける"]),
        ("明日", "あした", "tomorrow", ["ミョウニチ"], ["あした", "あす"]),
        ("明後日", "あさって", "day after tomorrow", [], ["あさって"]),
        ("朝", "あさ", "morning", ["チョウ"], ["あさ"]),
        ("下げる", "さげる", "to lower / hang", ["カ", "ゲ"], ["さ.げる", "くだ.る"]),
    ],
    # Lesson 2[cite: 21]
    [
        ("毎朝", "まいあさ", "every morning", ["マイチョウ"], []),
        ("今朝", "けさ", "this morning", [], ["けさ"]),
        ("曜", "よう", "day of the week", ["ヨウ"], []),
        ("日曜日", "にちようび", "Sunday", ["ニチヨウビ"], []),
        ("大分", "だいぶ", "considerably / fairly", ["ダイブ", "ダイブン"], []),
    ],
    # Lesson 3[cite: 21]
    [
        ("月曜日", "げつようび", "Monday", ["ゲツヨウビ"], []),
        ("火曜日", "かようび", "Tuesday", ["カヨウビ"], []),
        ("水曜日", "すいようび", "Wednesday", ["スイヨウビ"], []),
        ("木曜日", "もくようび", "Thursday", ["モクヨウビ"], []),
    ],
    # Lesson 4[cite: 21]
    [
        ("金曜日", "きんようび", "Friday", ["キンヨウビ"], []),
        ("土曜日", "どようび", "Saturday", ["ドヨウビ"], []),
        ("何曜日", "なんようび", "what day of the week", ["ナンヨウビ"], []),
        ("昼", "ひる", "daytime / noon", ["チュウ"], ["ひる"]),
    ],
    # Lesson 5[cite: 21]
    [
        ("昼間", "ひるま", "daytime", ["チュウカン"], ["ひるま"]),
        ("昼休み", "ひるやすみ", "lunch break", [], ["ひるやすみ"]),
        ("夜", "よる", "night / evening", ["ヤ"], ["よ", "よる"]),
        ("夜中", "よなか", "midnight", ["ヤチュウ"], ["よなか"]),
    ],
    # Lesson 6[cite: 21]
    [
        ("今夜", "こんや", "tonight", ["コンヤ"], []),
        ("夜行バス", "やこうバス", "overnight bus", ["ヤコウ"], []),
        ("夕べ", "ゆうべ", "last night / evening", ["セキ"], ["ゆう", "ゆうべ"]),
        ("去る", "さる", "to leave / pass", ["キョ", "コ"], ["さ.る"]),
    ],
    # Lesson 7[cite: 21]
    [
        ("去年", "きょねん", "last year", ["キョネン"], []),
        ("度", "ど", "degree / time", ["ド", "ト", "タク"], ["たび"]),
        ("今度", "こんど", "this time / next time", ["コンド"], []),
        ("一度", "いちど", "once / one time", ["イチド"], []),
    ],
    # Lesson 8[cite: 21]
    [
        ("一度も", "いちども", "not once / never", ["イチド"], []),
        ("春", "はる", "spring", ["シュン"], ["はる"]),
        ("夏", "なつ", "summer", ["カ", "ゲ"], ["なつ"]),
        ("秋", "あき", "autumn / fall", ["シュウ"], ["あき"]),
    ],
    # Lesson 9[cite: 21]
    [
        ("冬", "ふゆ", "winter", ["トウ"], ["ふゆ"]),
        ("色", "いろ", "color", ["ショク", "シキ"], ["いろ"]),
        ("赤い", "あかい", "red", ["セキ", "シャク"], ["あか", "あか.い"]),
        ("赤ちゃん", "あかちゃん", "baby", ["セキ"], ["あか"]),
    ],
    # Lesson 10[cite: 21]
    [
        ("青い", "あおい", "blue / green", ["セイ", "ショウ"], ["あお", "あお.い"]),
        ("青空", "あおぞら", "blue sky", ["セイクウ"], ["あおぞら"]),
        ("黒い", "くろい", "black", ["コク"], ["くろ", "くろ.い"]),
        ("家", "いえ", "house / home", ["カ", "ケ"], ["いえ", "や", "うち"]),
    ],
    # Lesson 11[cite: 21]
    [
        ("族", "ぞく", "tribe / family", ["ゾク"], []),
        ("家族", "かぞく", "family", ["カゾク"], []),
        ("親", "おや", "parent / intimacy", ["シン"], ["おや", "した.しい"]),
        ("親友", "しんゆう", "close friend", ["シンユウ"], []),
    ],
    # Lesson 12[cite: 21]
    [
        ("姉", "あね", "older sister", ["シ"], ["あね", "ねえ"]),
        ("お姉さん", "おねえさん", "older sister (polite)", ["シ"], ["ねえ"]),
        ("兄", "あに", "older brother", ["ケイ", "キョウ"], ["あに", "にい"]),
        ("お兄さん", "おにいさん", "older brother (polite)", ["ケイ"], ["にい"]),
    ],
    # Lesson 13[cite: 21]
    [
        ("弟", "おとうと", "younger brother", ["テイ", "ダイ", "デ"], ["おとうと"]),
        ("弟さん", "おとうとさん", "younger brother (polite)", ["テイ"], ["おとうと"]),
        ("兄弟", "きょうだい", "siblings / brothers", ["キョウダイ"], []),
        ("妹", "いもうと", "younger sister", ["マイ"], ["いもうと"]),
    ],
    # Lesson 14[cite: 21]
    [
        ("妹さん", "いもうとさん", "younger sister (polite)", ["マイ"], ["いもうと"]),
        ("主", "ぬし", "master / main", ["シュ", "ス"], ["ぬし", "おも"]),
        ("ご主人", "ごしゅじん", "husband (polite)", ["シュジン"], []),
        ("体", "からだ", "body", ["タイ", "テイ"], ["からだ"]),
    ],
    # Lesson 15[cite: 21]
    [
        ("心", "こころ", "heart / mind", ["シン"], ["こころ"]),
        ("安心", "あんしん", "relief / peace of mind", ["アンシン"], []),
        ("風", "かぜ", "wind / style", ["フウ", "フ"], ["かぜ", "かざ-"]),
        ("海", "うみ", "sea / ocean", ["カイ"], ["うみ"]),
    ],
    # Lesson 16[cite: 21]
    [
        ("海外", "かいがい", "overseas / abroad", ["カイガイ"], []),
        ("北海道", "ほっかいどう", "Hokkaido", ["ホッカイドウ"], []),
        ("銀", "ぎん", "silver", ["ギン"], []),
        ("銀行", "ぎんこう", "bank", ["ギンコウ"], []),
    ],
    # Lesson 17[cite: 21]
    [
        ("肉", "にく", "meat", ["ニク"], []),
        ("牛", "うし", "cow / cattle", ["ギュウ"], ["うし"]),
        ("牛肉", "ぎゅうにく", "beef", ["ギュウニク"], []),
        ("鳥", "とり", "bird / chicken", ["チョウ"], ["とり"]),
    ],
    # Lesson 18[cite: 21]
    [
        ("お茶", "おちゃ", "tea / green tea", ["チャ", "サ"], []),
        ("茶道", "さどう", "tea ceremony", ["サドウ", "チャドウ"], []),
        ("味", "あじ", "taste / flavor", ["ミ"], ["あじ", "あじ.わう"]),
    ],
    # Lesson 19[cite: 21]
    [
        ("ご飯", "ごはん", "cooked rice / meal", ["ハン"], ["めし"]),
        ("朝ご飯", "あさごはん", "breakfast", ["ハン"], ["あさ"]),
        ("昼ご飯", "ひるごはん", "lunch", ["ハン"], ["ひる"]),
        ("室", "しつ", "room", ["シツ"], ["むろ"]),
    ],
    # Lesson 20[cite: 21]
    [
        ("通り", "とおり", "street / avenue", ["ツウ"], ["とお.り"]),
        ("通う", "かよう", "to commute", ["ツウ"], ["かよ.う"]),
        ("通る", "とおる", "to pass through", ["ツウ"], ["とお.る"]),
        ("員", "いん", "member / staff", ["イン"], []),
    ],
    # Lesson 21[cite: 21]
    [
        ("店員", "てんいん", "store clerk", ["テンイン"], []),
        ("駅員", "えきいん", "station attendant", ["エキイン"], []),
        ("社員", "しゃいん", "company employee", ["シャイン"], []),
        ("会社員", "かいしゃいん", "office worker", ["カイシャイン"], []),
    ],
    # Lesson 22[cite: 21]
    [
        ("銀行員", "ぎんこういん", "bank clerk", ["ギンコウイン"], []),
        ("犬", "いぬ", "dog", ["ケン"], ["いぬ"]),
        ("歌", "うた", "song", ["カ"], ["うた", "うた.う"]),
        ("歌う", "うたう", "to sing", ["カ"], ["うた.う"]),
    ],
    # Lesson 23[cite: 21]
    [
        ("音", "おと", "sound / noise", ["オン", "イン"], ["おと", "ね"]),
        ("文", "ぶん", "sentence / writing", ["ブン", "モン"], ["ふみ"]),
        ("服", "ふく", "clothes", ["フク"], []),
    ],
    # Lesson 24[cite: 21]
    [
        ("医", "い", "medicine / doctor", ["イ"], []),
        ("医学", "いがく", "medical science", ["イガク"], []),
        ("旅", "たび", "travel / trip", ["リョ"], ["たび"]),
        ("旅行", "りょこう", "travel / trip", ["リョコウ"], []),
    ],
    # Lesson 25[cite: 21]
    [
        ("旅行社", "りょこうしゃ", "travel agency", ["リョコウシャ"], []),
        ("屋", "や", "roof / shop", ["オク"], ["や"]),
        ("屋上", "おくじょう", "rooftop", ["オクジョウ"], []),
        ("本屋", "ほんや", "bookstore", ["ホンヤ"], []),
    ],
    # Lesson 26[cite: 20]
    [
        ("名古屋", "なごや", "Nagoya", ["メイコオク"], ["なごや"]),
        ("英", "えい", "England / English", ["エイ"], []),
        ("字", "じ", "character / letter", ["ジ"], ["あざ"]),
        ("ローマ字", "ローマじ", "Roman letters / Romaji", ["ジ"], []),
        ("文字", "もじ", "letter / character", ["モジ", "モンジ"], []),
    ],
    # Lesson 27[cite: 20]
    [
        ("用", "よう", "business / use", ["ヨウ"], ["もち.いる"]),
        ("氷", "こおり", "ice", ["ヒョウ"], ["こおり", "ひ"]),
        ("会話", "かいわ", "conversation", ["カイワ"], []),
        ("仕", "し", "serve / official", ["シ", "ジ"], ["つか.える"]),
        ("英語", "えいご", "English language", ["エイゴ"], []),
    ],
    # Lesson 28[cite: 20]
    [
        ("院", "いん", "institution", ["イン"], []),
        ("入院", "にゅういん", "hospitalization", ["ニュウイン"], []),
        ("大学院", "だいがくいん", "graduate school", ["ダイガクイン"], []),
        ("使う", "つかう", "to use", ["シ"], ["つか.う"]),
    ],
    # Lesson 29[cite: 20]
    [
        ("町", "まち", "town / neighborhood", ["チョウ"], ["まち"]),
        ("物", "もの", "thing / object", ["ブツ", "モツ"], ["もの"]),
        ("本物", "ほんもの", "genuine article", ["ホンモノ"], []),
        ("見物", "けんぶつ", "sightseeing", ["ケンブツ"], []),
    ],
    # Lesson 30[cite: 20]
    [
        ("食べ物", "たべもの", "food", ["ショクモツ"], ["たべもの"]),
        ("飲み物", "のみもの", "drink / beverage", ["インショクブツ"], ["のみもの"]),
        ("買い物", "かいもの", "shopping", [], ["かいもの"]),
        ("正しい", "ただしい", "correct / right", ["セイ", "ショウ"], ["ただ.しい"]),
    ],
    # Lesson 31[cite: 20]
    [
        ("お正月", "おしょうがつ", "New Year", ["ショウガツ"], []),
        ("館", "かん", "building / hall", ["カン"], ["やかた"]),
        ("旅館", "りょかん", "Japanese inn", ["リョカン"], []),
        ("大使館", "たいしかん", "embassy", ["タイシカン"], []),
    ],
    # Lesson 32[cite: 20]
    [
        ("場", "ば", "place / location", ["ジョウ"], ["ば"]),
        ("スキー場", "スキーじょう", "ski resort", ["ジョウ"], []),
        ("会場", "かいじょう", "assembly hall / venue", ["カイジョウ"], []),
        ("味", "あじ", "taste / flavor", ["ミ"], ["あじ"]),
        ("立場", "たちば", "standpoint / position", ["リツジョウ"], ["たちば"]),
    ],
    # Lesson 33[cite: 20]
    [
        ("地下", "ちか", "underground / basement", ["チカ"], []),
        ("真", "ま", "true / reality", ["シン"], ["ま", "まこと"]),
        ("真ん中", "まんなか", "middle / center", ["シンチュウ"], ["まんなか"]),
        ("紙", "かみ", "paper", ["シ"], ["かみ"]),
    ],
    # Lesson 34[cite: 20]
    [
        ("手紙", "てがみ", "letter", ["シュシ"], ["てがみ"]),
        ("画", "が", "picture / stroke", ["ガ", "カク"], ["えが.く"]),
        ("悪い", "わるい", "bad", ["アク", "オ"], ["わる.い"]),
        ("気分が悪い", "きぶんがわるい", "to feel sick", ["キブン"], ["わる.い"]),
    ],
    # Lesson 35[cite: 20]
    [
        ("洋", "よう", "ocean / Western", ["ヨウ"], []),
        ("洋食", "ようしょく", "Western food", ["ヨウショク"], []),
        ("代", "だい", "substitute / generation", ["ダイ", "タイ"], ["か.わる", "よ"]),
        ("時代", "じだい", "era / period", ["ジダイ"], []),
    ],
    # Lesson 36[cite: 20]
    [
        ("図", "ず", "map / drawing", ["ズ", "ト"], ["え", "はか.る"]),
        ("地図", "ちず", "map", ["チズ"], []),
        ("図書館", "としょかん", "library", ["トショカン"], []),
        ("工", "こう", "craft / construction", ["コウ", "ク"], []),
    ],
    # Lesson 37[cite: 20]
    [
        ("工場", "こうじょう", "factory", ["コウジョウ"], []),
        ("界", "かい", "world / boundary", ["カイ"], []),
        ("世界", "せかい", "the world", ["セカイ"], []),
        ("世界中", "せかいじゅう", "around the world", ["セカイジュウ"], []),
    ],
    # Lesson 38[cite: 20]
    [
        ("堂", "どう", "public chamber / hall", ["ドウ"], []),
        ("食堂", "しょくどう", "dining hall / cafeteria", ["ショクドウ"], []),
        ("病", "やまい", "illness / disease", ["ビョウ", "ヘイ"], ["や.む", "やまい"]),
        ("病院", "びょういん", "hospital", ["ビョウイン"], []),
    ],
    # Lesson 39[cite: 20]
    [
        ("病気", "びょうき", "illness / sickness", ["ビョウキ"], []),
        ("理", "り", "logic / reason", ["リ"], ["ことわり"]),
        ("料理", "りょうり", "cooking / cuisine", ["リョウリ"], []),
        ("漢", "かん", "Sino- / China", ["カン"], []),
    ],
    # Lesson 40[cite: 20]
    [
        ("漢字", "かんじ", "Kanji", ["カンジ"], []),
        ("元", "もと", "origin / base", ["ゲン", "ガン"], ["もと"]),
        ("元日", "がんじつ", "New Year's Day", ["ガンジツ"], []),
        ("意", "い", "idea / mind", ["イ"], []),
    ],
    # Lesson 41[cite: 20]
    [
        ("意味", "いみ", "meaning", ["イミ"], []),
        ("意見", "いけん", "opinion", ["イケン"], []),
        ("用意", "ようい", "preparation", ["ヨウイ"], []),
        ("野", "の", "plains / field", ["ヤ", "ショ"], ["の"]),
    ],
    # Lesson 42[cite: 20]
    [
        ("上野", "うえの", "Ueno", ["ジョウヤ"], ["うえの"]),
        ("京", "きょう", "capital", ["キョウ", "ケイ"], ["みやこ"]),
        ("東京", "とうきょう", "Tokyo", ["トウキョウ"], []),
        ("開く", "あく", "to open (intransitive)", ["カイ"], ["あ.く", "ひら.く"]),
    ],
    # Lesson 43[cite: 20]
    [
        ("開く", "ひらく", "to open / hold an event", ["カイ"], ["ひら.く"]),
        ("開ける", "あける", "to open (transitive)", ["カイ"], ["あ.ける"]),
        ("歩く", "あるく", "to walk", ["ホ", "ブ", "フ"], ["ある.く", "あゆ.む"]),
        ("走る", "はしる", "to run", ["ソウ"], ["はし.る"]),
    ],
    # Lesson 44[cite: 20]
    [
        ("止む", "やむ", "to cease / stop", ["シ"], ["と.まる", "や.む"]),
        ("止める", "とめる", "to stop (something)", ["シ"], ["と.める"]),
        ("中止", "ちゅうし", "cancellation / suspension", ["チュウシ"], []),
    ],
    # Lesson 45[cite: 20]
    [
        ("売る", "うる", "to sell", ["バイ"], ["う.る", "う.れる"]),
        ("売れる", "うれる", "to sell well", ["バイ"], ["う.れる"]),
        ("売り場", "うりば", "sales floor / counter", ["バイジョウ"], ["うりば"]),
        ("計る", "はかる", "to measure / weigh", ["ケイ"], ["はか.る"]),
        ("売上", "うりあげ", "sales / revenue", ["バイジョウ"], ["うりあげ"]),
    ],
    # Lesson 46[cite: 20]
    [
        ("時計", "とけい", "watch / clock", ["トケイ"], []),
        ("計画", "けいかく", "plan / project", ["ケイカク"], []),
        ("住む", "すむ", "to live / reside", ["ジュウ"], ["す.む"]),
        ("待つ", "まつ", "to wait", ["タイ"], ["ま.つ"]),
    ],
    # Lesson 47[cite: 20]
    [
        ("始まる", "はじまる", "to begin (intransitive)", ["シ"], ["はじ.まる"]),
        ("始める", "はじめる", "to start (transitive)", ["シ"], ["はじ.める"]),
        ("起きる", "おきる", "to wake up / happen", ["キ"], ["お.きる", "お.こる"]),
        ("起こる", "おこる", "to occur / happen", ["キ"], ["お.こる"]),
    ],
    # Lesson 48[cite: 20]
    [
        ("起こす", "おこす", "to wake someone up", ["キ"], ["お.こす"]),
        ("答え", "こたえ", "answer / response", ["トウ"], ["こた.え"]),
        ("答える", "こたえる", "to answer", ["トウ"], ["こた.える"]),
        ("持つ", "もつ", "to hold / carry", ["ジ"], ["も.つ"]),
        ("気持ち", "きもち", "feeling / mood", ["キモチ"], []),
    ],
    # Lesson 49[cite: 20]
    [
        ("着く", "つく", "to arrive", ["チャク", "ジャク"], ["き.る", "つ.く"]),
        ("着る", "きる", "to wear (upper body)", ["チャク"], ["き.る"]),
        ("上着", "うわぎ", "coat / jacket", ["ジョウチャク"], ["うわぎ"]),
        ("下着", "したぎ", "underwear", ["カチャク"], ["したぎ"]),
    ],
    # Lesson 50[cite: 20]
    [
        ("着物", "きもの", "kimono / clothing", ["チャクブツ"], ["きもの"]),
        ("教える", "おしえる", "to teach / tell", ["キョウ"], ["おし.える"]),
        ("教会", "きょうかい", "church", ["キョウカイ"], []),
        ("教室", "きょうしつ", "classroom", ["キョウシツ"], []),
    ],
    # Lesson 51[cite: 22]
    [
        ("動く", "うごく", "to move (intransitive)", ["ドウ"], ["うご.く"]),
        ("動かす", "うごかす", "to move (transitive)", ["ドウ"], ["うご.かす"]),
        ("動物", "どうぶつ", "animal", ["ドウブツ"], []),
        ("集める", "あつめる", "to collect / gather", ["シュウ"], ["あつ.める", "あつ.まる"]),
    ],
    # Lesson 52[cite: 22]
    [
        ("借りる", "かりる", "to borrow / rent", ["シャク"], ["か.りる"]),
        ("死ぬ", "しぬ", "to die", ["シ"], ["し.ぬ"]),
        ("習う", "ならう", "to learn", ["シュウ"], ["なら.う"]),
        ("注ぐ", "そそぐ", "to pour / water", ["チュウ"], ["そそ.ぐ"]),
    ],
    # Lesson 53[cite: 22]
    [
        ("注文", "ちゅうもん", "order (food/goods)", ["チュウモン"], []),
        ("注意", "ちゅうい", "caution / attention", ["チュウイ"], []),
        ("急ぐ", "いそぐ", "to hurry", ["キュウ"], ["いそ.ぐ"]),
        ("急行", "きゅうこう", "express train", ["キュウコウ"], []),
    ],
    # Lesson 54[cite: 22]
    [
        ("建つ", "たつ", "to be built", ["ケン", "コン"], ["た.つ", "た.てる"]),
        ("建てる", "たてる", "to build / construct", ["ケン"], ["た.てる"]),
        ("建物", "たてもの", "building", ["ケンブツ"], ["たてもの"]),
        ("終わり", "おわり", "the end", ["シュウ"], ["お.わり"]),
    ],
    # Lesson 55[cite: 22]
    [
        ("終わる", "おわる", "to end / finish", ["シュウ"], ["お.わる"]),
        ("勉", "べん", "exertion / diligence", ["ベン"], ["つと.める"]),
        ("思う", "おもう", "to think / feel", ["シ"], ["おも.う"]),
        ("思い出す", "おもいだす", "to recall / remember", ["シシュツ"], ["おもいだ.す"]),
    ],
    # Lesson 56[cite: 22]
    [
        ("考える", "かんがえる", "to think / consider", ["コウ"], ["かんが.える"]),
        ("知る", "しる", "to know", ["チ"], ["し.る"]),
        ("知らせる", "しらせる", "to notify / inform", ["チ"], ["し.らせる"]),
        ("写す", "うつす", "to copy / photograph", ["シャ", "ジャ"], ["うつ.す"]),
    ],
    # Lesson 57[cite: 22]
    [
        ("写真", "しゃしん", "photograph", ["シャシン"], []),
        ("映す", "うつす", "to project / reflect", ["エイ"], ["うつ.す", "うつ.る"]),
        ("映画", "えいが", "movie / film", ["エイガ"], []),
        ("映画館", "えいがかん", "movie theater", ["エイガカン"], []),
    ],
    # Lesson 58[cite: 22]
    [
        ("作る", "つくる", "to make / create", ["サク", "サ"], ["つく.る"]),
        ("作文", "さくぶん", "essay / composition", ["サクブン"], []),
        ("試す", "ためす", "to try / test", ["シ"], ["ため.す", "こころ.みる"]),
        ("帰り", "かえり", "return / coming home", ["キ"], ["かえ.り"]),
    ],
    # Lesson 59[cite: 22]
    [
        ("帰る", "かえる", "to return home", ["キ"], ["かえ.る"]),
        ("お帰りなさい", "おかえりなさい", "welcome home", ["キ"], ["かえ.り"]),
        ("帰国", "きこく", "return to one's country", ["キコク"], []),
        ("切る", "きる", "to cut", ["セツ", "サイ"], ["き.る", "き.れる"]),
    ],
    # Lesson 60[cite: 22]
    [
        ("切れる", "きれる", "to cut well / expire", ["セツ"], ["き.れる"]),
        ("切手", "きって", "postage stamp", ["セッシュ"], ["きって"]),
        ("親切", "しんせつ", "kind / gentle", ["シンセツ"], []),
        ("大切", "たいせつ", "important / precious", ["タイセツ"], []),
    ],
    # Lesson 61[cite: 22]
    [
        ("者", "もの", "person / someone", ["シャ"], ["もの"]),
        ("医者", "いしゃ", "doctor", ["イシャ"], []),
        ("お医者さん", "おいしゃさん", "doctor (polite)", ["イシャ"], []),
        ("転ぶ", "ころぶ", "to fall down", ["テン"], ["ころ.ぶ", "ころ.がる"]),
    ],
    # Lesson 62[cite: 22]
    [
        ("貸す", "かす", "to lend", ["タイ"], ["か.す"]),
        ("送る", "おくる", "to send", ["ソウ"], ["おく.る"]),
        ("別れる", "わかれる", "to part / separate", ["ベツ"], ["わか.れる"]),
        ("運ぶ", "はこぶ", "to carry / transport", ["ウン"], ["はこ.ぶ"]),
        ("別", "べつ", "separate / another", ["ベツ"], ["わか.れる"]),
    ],
    # Lesson 63[cite: 22]
    [
        ("運転", "うんてん", "driving", ["ウンテン"], []),
        ("運動", "うんどう", "exercise / motion", ["ウンドウ"], []),
        ("運転手", "うんてんしゅ", "driver", ["ウンテンシュ"], []),
        ("重い", "おもい", "heavy / serious", ["ジュウ", "チョウ"], ["おも.い", "かさ.ねる"]),
    ],
    # Lesson 64[cite: 22]
    [
        ("体重", "たいじゅう", "body weight", ["タイジュウ"], []),
        ("楽", "らく", "comfort / ease", ["ガク", "ラク"], ["たの.しい"]),
        ("楽しむ", "たのしむ", "to enjoy", ["ラク"], ["たの.しむ"]),
        ("楽しい", "たのしい", "fun / enjoyable", ["ラク"], ["たの.しい"]),
    ],
    # Lesson 65[cite: 22]
    [
        ("音楽", "おんがく", "music", ["オンガク"], []),
        ("早い", "はやい", "early / fast", ["ソウ", "サッ"], ["はや.い"]),
        ("早く", "はやく", "early / quickly", ["ソウ"], ["はや.く"]),
        ("早起き", "はやおき", "early rising", ["ソウキ"], ["はやおき"]),
    ],
    # Lesson 66[cite: 22]
    [
        ("広い", "ひろい", "wide / spacious", ["コウ"], ["ひろ.い"]),
        ("広場", "ひろば", "public square / plaza", ["コウジョウ"], ["ひろば"]),
        ("強い", "つよい", "strong / powerful", ["キョウ", "ゴウ"], ["つよ.い"]),
        ("勉強", "べんきょう", "study", ["ベンキョウ"], []),
    ],
    # Lesson 67[cite: 22]
    [
        ("勉強中", "べんきょうちゅう", "currently studying", ["ベンキョウチュウ"], []),
        ("近い", "ちかい", "near / close", ["キン", "コン"], ["ちか.い"]),
        ("近く", "ちかく", "nearby / neighborhood", ["キン"], ["ちか.く"]),
        ("公", "こう", "public / official", ["コウ", "ク"], ["おおやけ"]),
    ],
    # Lesson 68[cite: 22]
    [
        ("有", "ゆう", "existence / possession", ["ユウ", "ウ"], ["あ.る"]),
        ("有名", "ゆうめい", "famous", ["ユウメイ"], []),
        ("不", "ふ", "negative / un- / non-", ["フ", "ブ"], []),
        ("以", "い", "by means of / because", ["イ"], ["もっ.て"]),
    ],
    # Lesson 69[cite: 22]
    [
        ("以上", "いじょう", "more than / above", ["イジョウ"], []),
        ("以下", "いか", "less than / below", ["イカ"], []),
        ("以外", "いがい", "except / other than", ["イガイ"], []),
        ("同じ", "おなじ", "same / identical", ["ドウ"], ["おな.じ"]),
    ],
    # Lesson 70[cite: 22]
    [
        ("自", "じ", "oneself", ["ジ", "シ"], ["みずか.ら"]),
        ("自分で", "じぶんで", "by oneself", ["ジブン"], []),
        ("自動車", "じどうしゃ", "automobile / car", ["ジドウシャ"], []),
        ("自転車", "じてんしゃ", "bicycle", ["ジテンシャ"], []),
        ("自分", "じぶん", "oneself / myself", ["ジブン"], []),
    ],
    # Lesson 71[cite: 23]
    [
        ("方", "かた", "direction / person / way", ["ホウ"], ["かた"]),
        ("あの方", "あのかた", "that person (polite)", ["ホウ"], ["かた"]),
        ("夕方", "ゆうがた", "evening / dusk", ["セキホウ"], ["ゆうがた"]),
        ("仕方", "しかた", "way / method", ["シカタ"], []),
    ],
    # Lesson 72[cite: 23]
    [
        ("方言", "ほうげん", "dialect", ["ホウゲン"], []),
        ("研", "けん", "polish / study", ["ケン"], ["と.ぐ"]),
        ("究", "きゅう", "research / study", ["キュウ", "ク"], ["きわ.める"]),
        ("研究", "けんきゅう", "research", ["ケンキュウ"], []),
    ],
    # Lesson 73[cite: 23]
    [
        ("研究室", "けんきゅうしつ", "laboratory / professor's office", ["ケンキュウシツ"], []),
        ("題", "だい", "topic / subject", ["ダイ"], []),
        ("事", "こと", "thing / matter", ["ジ", "ズ"], ["こと"]),
        ("家事", "かじ", "housework", ["カジ"], []),
    ],
    # Lesson 74[cite: 23]
    [
        ("火事", "かじ", "fire (disaster)", ["カジ"], []),
        ("用事", "ようじ", "errand / business", ["ヨウジ"], []),
        ("仕事", "しごと", "work / job", ["シゴト"], []),
        ("食事", "しょくじ", "meal", ["ショクジ"], []),
    ],
    # Lesson 75[cite: 23]
    [
        ("大事", "だいじ", "important / valuable", ["ダイジ"], []),
        ("特に", "とくに", "especially / particularly", ["トク"], []),
        ("特急", "とっきゅう", "limited express train", ["トッキュウ"], []),
        ("特別", "とくべつ", "special", ["トクベツ"], []),
    ],
    # Lesson 76[cite: 23]
    [
        ("無", "む", "nothingness / none", ["ム", "ブ"], ["な.い"]),
        ("無理", "むり", "impossible / unreasonable", ["ムリ"], []),
        ("品", "しな", "goods / article", ["ヒン", "ホン"], ["しな"]),
        ("質", "しつ", "quality / substance", ["シツ", "シチ"], ["たち"]),
        ("無くなる", "なくなる", "to run out / be lost", ["ム"], ["な.くなる"]),
    ],
    # Lesson 77[cite: 23]
    [
        ("軽い", "かるい", "light (weight)", ["ケイ"], ["かる.い", "かろ.やか"]),
        ("問題", "もんだい", "problem / question", ["モンダイ"], []),
        ("質問", "しつもん", "question", ["シツモン"], []),
        ("的", "てき", "target / -like", ["テキ"], ["まと"]),
    ],
    # Lesson 78[cite: 23]
    [
        ("目的", "もくてき", "purpose / goal", ["モクテキ"], []),
        ("可", "か", "possible / passable", ["カ", "コク"], []),
        ("料", "りょう", "fee / material", ["リョウ"], []),
        ("無料", "むりょう", "free of charge", ["ムリョウ"], []),
    ],
    # Lesson 79[cite: 23]
    [
        ("有料", "ゆうりょう", "fee-charging / toll", ["ユウリョウ"], []),
        ("料理", "りょうり", "cooking / dish", ["リョウリ"], []),
        ("食料品", "しょくりょうひん", "groceries / foodstuffs", ["ショクリョウヒン"], []),
        ("料理教室", "りょうりきょうしつ", "cooking class", ["リョウリキョウシツ"], []),
    ],
    # Lesson 80[cite: 23]
    [
        ("業", "ぎょう", "business / industry", ["ギョウ", "ゴウ"], ["わざ"]),
        ("発", "はつ", "departure / emit", ["ハツ", "ホツ"], []),
        ("発音", "はつおん", "pronunciation", ["ハツオン"], []),
        ("出発", "しゅっぱつ", "departure", ["シュッパツ"], []),
    ],
    # Lesson 81[cite: 23]
    [
        ("始発", "しはつ", "first train/bus", ["シハツ"], []),
        ("身", "み", "body / oneself", ["シン"], ["み"]),
        ("身長", "しんちょう", "height (stature)", ["シンチョウ"], []),
        ("台", "だい", "stand / counter for machines", ["ダイ", "タイ"], ["うてな"]),
    ],
    # Lesson 82[cite: 23]
    [
        ("台風", "たいふう", "typhoon", ["タイフウ"], []),
        ("一台", "いちだい", "one (machine/vehicle)", ["イチダイ"], []),
        ("二台", "にだい", "two (machines/vehicles)", ["ニダイ"], []),
        ("三台", "さんだい", "three (machines/vehicles)", ["サンダイ"], []),
    ],
    # Lesson 83[cite: 23]
    [
        ("四台", "よんだい", "four (machines/vehicles)", ["ヨンダイ"], []),
        ("五台", "ごだい", "five (machines/vehicles)", ["ゴダイ"], []),
        ("六台", "ろくだい", "six (machines/vehicles)", ["ロクダイ"], []),
        ("七台", "ななだい", "seven (machines/vehicles)", ["ナナダイ"], []),
    ],
    # Lesson 84[cite: 23]
    [
        ("八台", "はちだい", "eight (machines/vehicles)", ["ハチダイ"], []),
        ("九台", "きゅうだい", "nine (machines/vehicles)", ["キュウダイ"], []),
        ("十台", "じゅうだい", "ten (machines/vehicles)", ["ジュウダイ"], []),
        ("水道", "すいどう", "water supply", ["スイドウ"], []),
    ],
    # Lesson 85[cite: 23]
    [
        ("遠足", "えんそく", "excursion / field trip", ["エンソク"], []),
        ("出す", "だす", "to take out / send", ["シュツ"], ["だ.す"]),
        ("外に", "そとに", "outside", ["ガイ"], ["そと"]),
        ("大学生", "だいがくせい", "university student", ["ダイガクセイ"], []),
    ],
    # Lesson 86[cite: 23]
    [
        ("その上", "そのうえ", "moreover / besides", ["ジョウ"], ["うえ"]),
        ("行き", "いき", "bound for / going", ["コウ"], ["い.き", "ゆ.き"]),
        ("十分", "じゅうぶん", "enough / sufficient", ["ジュウブン"], []),
        ("生け花", "いけばな", "flower arrangement", ["セイカ"], ["いけばな"]),
    ],
    # Lesson 87[cite: 23]
    [
        ("半分", "はんぶん", "half", ["ハンブン"], []),
        ("今にも", "いまにも", "at any moment", ["コン"], ["いま"]),
        ("お子さん", "おこさん", "someone's child (polite)", ["シ"], ["こ"]),
        ("駅前", "えきまえ", "in front of the station", ["エキマエ"], []),
    ],
    # Lesson 88[cite: 23]
    [
        ("空く", "すく", "to become empty/less crowded", ["クウ"], ["す.く", "あ.く"]),
        ("立てる", "たてる", "to stand something up", ["リツ"], ["た.てる"]),
        ("人力", "じんりょく", "human power", ["ジンリョク"], []),
        ("この間", "このあいだ", "the other day / recently", ["カン"], ["あいだ"]),
    ],
    # Lesson 89[cite: 23]
    [
        ("ある日", "あるひ", "one day", ["ニチ"], ["ひ"]),
        ("見学", "けんがく", "study visit / field trip", ["ケンガク"], []),
        ("大きな", "おおきな", "big / large", ["ダイ"], ["おお.きな"]),
        ("入学", "にゅうがく", "school admission", ["ニュウガク"], []),
    ],
    # Lesson 90[cite: 23]
    [
        ("入り口", "いりぐち", "entrance", ["ニュウコウ"], ["いりぐち"]),
        ("空く", "あく", "to become vacant / open", ["クウ"], ["あ.く"]),
        ("毎月", "まいつき", "every month", ["マイゲツ"], ["まいつき"]),
        ("足りる", "たりる", "to be sufficient / enough", ["ソク"], ["た.りる"]),
    ],
    # Lesson 91[cite: 23]
    [
        ("空気", "くうき", "air / atmosphere", ["クウキ"], []),
        ("新聞社", "しんぶんしゃ", "newspaper company", ["シンブンシャ"], []),
        ("見える", "みえる", "to be visible", ["ケン"], ["み.える"]),
        ("社長", "しゃちょう", "company president", ["シャチョウ"], []),
    ],
    # Lesson 92[cite: 23]
    [
        ("お金を下ろす", "おかねをおろす", "to withdraw money", ["キン"], ["かね", "お.ろす"]),
        ("聞こえる", "きこえる", "to be audible / can hear", ["ブン"], ["き.こえる"]),
        ("毎年", "まいとし", "every year", ["マイネン"], ["まいとし"]),
        ("大会", "たいかい", "tournament / convention", ["タイカイ"], []),
    ],
    # Lesson 93[cite: 23]
    [
        ("上がる", "あがる", "to rise / go up", ["ジョウ"], ["あ.がる"]),
        ("本社", "ほんしゃ", "head office", ["ホンシャ"], []),
        ("人口", "じんこう", "population", ["ジンコウ"], []),
        ("生きる", "いきる", "to live / be alive", ["セイ", "ショウ"], ["い.きる"]),
    ],
    # Lesson 94[cite: 23]
    [
        ("気分", "きぶん", "feeling / mood", ["キブン"], []),
        ("人気", "にんき", "popularity", ["ニンキ"], []),
        ("外れる", "はずれる", "to come off / miss", ["ガイ"], ["はず.れる"]),
        ("毎週", "まいしゅう", "every week", ["マイシュウ"], []),
    ],
    # Lesson 95[cite: 23]
    [
        ("行う", "おこなう", "to perform / carry out", ["コウ"], ["おこな.う"]),
        ("小さな", "ちいさな", "small / little", ["ショウ"], ["ちい.さな"]),
        ("何台", "なんだい", "how many (machines/vehicles)", ["ナンダイ"], []),
        ("写す", "うつす", "to copy / transcribe", ["シャ"], ["うつ.す"]),
        ("映す", "うつす", "to project (on a screen)", ["エイ"], ["うつ.す"]),
    ],
]


def get_strokes_for_char(ch: str) -> list[str]:
    """Reads the 5-digit Unicode hex SVG from KanjiVG and extracts SVG path 'd' strings."""
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
        raise FileNotFoundError(
            f"Could not find '{KANJIVG_DIR}'. Make sure KanjiVG 'kanji' folder is extracted there."
        )

    lessons = []
    item_counter = 1

    for l_idx, chunk in enumerate(N4_LESSONS_DATA):
        lesson_num = l_idx + 1
        lesson_items = []

        for word, kana, meaning, onyomi, kunyomi in chunk:
            characters_data = []
            for ch in word:
                strokes = get_strokes_for_char(ch)
                characters_data.append({
                    "char": ch,
                    "strokes": strokes,
                })

            lesson_items.append({
                "id": f"n4-{item_counter}",
                "level": "N4",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n4-lesson-{lesson_num}",
            "level": "N4",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    os.makedirs(os.path.dirname(OUTPUT_TS_PATH), exist_ok=True)
    ts_content = (
        "import type { KanjiLesson } from '../types/kanji';\n\n"
        f"export const N4_LESSONS: KanjiLesson[] = {json.dumps(lessons, ensure_ascii=False, indent=2)};\n"
    )

    with open(OUTPUT_TS_PATH, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"Done! Generated {len(lessons)} N4 lessons ({item_counter - 1} items) in {OUTPUT_TS_PATH}.")


if __name__ == "__main__":
    main()