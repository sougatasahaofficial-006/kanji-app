import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n3_part1.json"
OUTPUT_TS_PATH = os.path.join("src", "data", "n3.ts")

N3_PART2_DATA = [
    # Lesson 176[cite: 27]
    [
        ("北半球", "きたはんきゅう", "Northern Hemisphere", ["キタハンキュウ"], []),
        ("南半球", "みなみはんきゅう", "Southern Hemisphere", ["ミナミハンキュウ"], []),
        ("お酒", "おさけ", "alcohol / sake", ["シュ"], ["さけ"]),
        ("飲酒", "いんしゅ", "drinking alcohol", ["インシュ"], []),
    ],
    # Lesson 177[cite: 27]
    [
        ("居酒屋", "いざかや", "Japanese-style pub", ["イザカヤ"], []),
        ("飲酒運転", "いんしゅうんてん", "drunk driving", ["インシュウンテン"], []),
        ("君", "きみ", "you (familiar)", ["クン"], ["きみ"]),
        ("察する", "さっする", "to guess / sense / sympathize", ["サツ"], ["さっ.する"]),
    ],
    # Lesson 178[cite: 27]
    [
        ("観察", "かんさつ", "observation", ["カンサツ"], []),
        ("警察官", "けいさつかん", "police officer", ["ケイサツカン"], []),
        ("望み", "のぞみ", "wish / hope / desire", ["ボウ", "モウ"], ["のぞ.み"]),
        ("望む", "のぞむ", "to desire / wish for", ["ボウ"], ["のぞ.む"]),
    ],
    # Lesson 179[cite: 27]
    [
        ("婚", "こん", "marriage", ["コン"], []),
        ("婚約", "こんやく", "engagement / betrothal", ["コンヤク"], []),
        ("単に", "たんに", "simply / merely", ["タン"], []),
        ("単なる", "たんなる", "mere / simple", ["タン"], []),
    ],
    # Lesson 180[cite: 27]
    [
        ("単語", "たんご", "word / vocabulary", ["タンゴ"], []),
        ("押す", "おす", "to push / press", ["オウ"], ["お.す", "お.さえる"]),
        ("押し入れ", "おしいれ", "closet", [], ["おしいれ"]),
        ("割る", "わる", "to divide / break / split", ["カツ"], ["わ.る", "わ.れる"]),
        ("分割", "ぶんかつ", "division / partitioning", ["ブンカツ"], []),
    ],
    # Lesson 181[cite: 27]
    [
        ("割れる", "われる", "to break / be divided", ["カツ"], ["わ.れる"]),
        ("割引", "わりびき", "discount", [], ["わりびき"]),
        ("役割", "やくわり", "part / role / duty", ["ヤクワリ"], []),
        ("割り込み", "わりこみ", "cutting in line / interruption", [], ["わりこみ"]),
    ],
    # Lesson 182[cite: 27]
    [
        ("割り引く", "わりびく", "to give a discount", [], ["わりび.く"]),
        ("割り込む", "わりこむ", "to cut in / interrupt", [], ["わりこ.む"]),
        ("時間割", "じかんわり", "timetable / schedule", ["ジカンワリ"], []),
        ("学生割引", "がくせいわりびき", "student discount", ["ガクセイワリビキ"], []),
    ],
    # Lesson 183[cite: 27]
    [
        ("限る", "かぎる", "to restrict / limit", ["ゲン"], ["かぎ.る"]),
        ("期限", "きげん", "term / period / deadline", ["キゲン"], []),
        ("限界", "げんかい", "limit / boundary", ["ゲンカイ"], []),
        ("戻る", "もどる", "to turn back / return", ["レイ"], ["もど.る", "もど.す"]),
    ],
    # Lesson 184[cite: 27]
    [
        ("戻す", "もどす", "to put back / return", ["レイ"], ["もど.す"]),
        ("科", "か", "department / course / section", ["カ"], []),
        ("科学", "かがく", "science", ["カガク"], []),
        ("教科", "きょうか", "school subject / curriculum", ["キョウカ"], []),
    ],
    # Lesson 185[cite: 27]
    [
        ("理科", "りか", "science (school subject)", ["リカ"], []),
        ("科目", "かもく", "subject / course", ["カモク"], []),
        ("学科", "がっか", "academic department / subject", ["ガッカ"], []),
        ("内科", "ないか", "internal medicine", ["ナイカ"], []),
    ],
    # Lesson 186[cite: 27]
    [
        ("外科", "げか", "surgery", ["ゲカ"], []),
        ("求める", "もとめる", "to seek / request / demand", ["キュウ"], ["もと.める"]),
        ("談", "だん", "discussion / talk", ["ダン"], []),
        ("相談", "そうだん", "consultation / discussion", ["ソウダン"], []),
    ],
    # Lesson 187[cite: 27]
    [
        ("降る", "ふる", "to fall (rain/snow)", ["コウ"], ["ふ.る", "お.りる"]),
        ("降りる", "おりる", "to get off / descend", ["コウ"], ["お.りる"]),
        ("以降", "いこう", "on and after / hereafter", ["イコウ"], []),
        ("降車口", "こうしゃぐち", "exit (bus/train)", ["コウシャグチ"], []),
    ],
    # Lesson 188[cite: 27]
    [
        ("妻", "つま", "wife", ["サイ"], ["つま"]),
        ("夫妻", "ふさい", "husband and wife / couple", ["フサイ"], []),
        ("両", "りょう", "both", ["リョウ"], []),
        ("福岡", "ふくおか", "Fukuoka Prefecture", ["フクオカ"], []),
    ],
    # Lesson 189[cite: 27]
    [
        ("熱", "ねつ", "heat / fever / passion", ["ネツ"], ["あつ.い"]),
        ("熱する", "ねっする", "to heat / get excited", ["ネツ"], ["ねっ.する"]),
        ("熱心", "ねっしん", "zealous / enthusiastic", ["ネッシン"], []),
        ("浮く", "うく", "to float / become loose", ["フ"], ["う.く", "う.かぶ"]),
        ("熱い", "あつい", "hot (to the touch)", ["ネツ"], ["あつ.い"]),
    ],
    # Lesson 190[cite: 27]
    [
        ("浮かぶ", "うかぶ", "to float / come to mind", ["フ"], ["う.かぶ"]),
        ("等", "とう", "etc. / class / equal", ["トウ"], ["ひと.しい"]),
        ("等しい", "ひとしい", "equal / identical", ["トウ"], ["ひと.しい"]),
        ("彼等", "かれら", "they / them", [], ["かれら"]),
        ("浮上", "ふじょう", "surfacing / rising", ["フジョウ"], []),
    ],
    # Lesson 191[cite: 27]
    [
        ("平等", "びょうどう", "equality / impartiality", ["ビョウドウ"], []),
        ("上等", "じょうとう", "first-class / very good", ["ジョウトウ"], []),
        ("高等学校", "こうとうがっこう", "senior high school", ["コウトウガッコウ"], []),
        ("末", "すえ", "end / tip / youngest", ["マツ", "バツ"], ["すえ"]),
        ("週末", "しゅうまつ", "weekend", ["シュウマツ"], []),
    ],
    # Lesson 192[cite: 26]
    [
        ("月末", "げつまつ", "end of the month", ["ゲツマツ"], []),
        ("末っ子", "すえっこ", "youngest child", [], ["すえっこ"]),
        ("年末年始", "ねんまつねんし", "year-end and New Year", ["ネンマツネンシ"], []),
        ("幸せ", "しあわせ", "happiness / good fortune", ["コウ"], ["しあわ.せ", "さいわ.い"]),
    ],
    # Lesson 193[cite: 26]
    [
        ("幸い", "さいわい", "fortunately / happiness", ["コウ"], ["さいわ.い"]),
        ("幸福", "こうふく", "happiness / well-being", ["コウフク"], []),
        ("草", "くさ", "grass / weed", ["ソウ"], ["くさ"]),
        ("越える", "こえる", "to cross over / exceed", ["エツ"], ["こ.える", "こ.す"]),
        ("引越し", "ひっこし", "moving (house)", [], ["ひっこし"]),
    ],
    # Lesson 194[cite: 26]
    [
        ("引っ越し", "ひっこし", "moving (house)", [], ["ひっこし"]),
        ("追い越す", "おいこす", "to pass / overtake", [], ["おいこ.す"]),
        ("乗り越す", "のりこす", "to ride past one's station", [], ["のりこ.す"]),
        ("乗り越し料金", "のりこしりょうきん", "excess fare", [], ["のりこしりょうきん"]),
    ],
    # Lesson 195[cite: 26]
    [
        ("登る", "のぼる", "to climb / ascend", ["トウ", "ト"], ["のぼ.る"]),
        ("登場", "とうじょう", "appearance (on stage/scene)", ["トウジョウ"], []),
        ("山登り", "やまのぼり", "mountain climbing", [], ["やまのぼり"]),
        ("類", "るい", "kind / sort / class", ["ルイ"], ["たぐ.い"]),
        ("登山", "とざん", "mountain climbing", ["トザン"], []),
    ],
    # Lesson 196[cite: 26]
    [
        ("書類", "しょるい", "documents / papers", ["ショルイ"], []),
        ("親類", "しんるい", "relative / relation", ["シンルイ"], []),
        ("種類", "しゅるい", "variety / kind / type", ["シュルイ"], []),
        ("未だ", "いまだ", "as yet / still", ["ミ"], ["いま.だ"]),
        ("未だに", "いまだに", "still / even now", ["ミ"], ["いま.だに"]),
    ],
    # Lesson 197[cite: 26]
    [
        ("未来", "みらい", "future", ["ミライ"], []),
        ("未成年", "みせいねん", "minor / underage", ["ミセイネン"], []),
        ("未開発", "みかいはつ", "undeveloped", ["ミカイハツ"], []),
        ("未使用", "みしよう", "unused", ["ミシヨウ"], []),
    ],
    # Lesson 198[cite: 26]
    [
        ("未解決", "みかいけつ", "unsolved / unsettled", ["ミカイケツ"], []),
        ("規", "き", "standard / measure / rule", ["キ"], []),
        ("定規", "じょうぎ", "ruler (measuring)", ["ジョウギ"], []),
        ("精", "せい", "refined / spirit / energy", ["セイ", "ショウ"], []),
    ],
    # Lesson 199[cite: 26]
    [
        ("抱く", "だく", "to hug / hold / embrace", ["ホウ"], ["だ.く", "いだ.く", "かか.える"]),
        ("抱っこ", "だっこ", "hug / carrying in arms", [], ["だっこ"]),
        ("労る", "いたわる", "to care for / console", ["ロウ"], ["いたわ.る"]),
        ("苦労", "くろう", "hardship / trouble", ["クロウ"], []),
        ("労働", "ろうどう", "manual labor / work", ["ロウドウ"], []),
    ],
    # Lesson 200[cite: 26]
    [
        ("処する", "しょする", "to deal with / manage", ["ショ"], ["しょ.する"]),
        ("処理", "しょり", "processing / disposal", ["ショリ"], []),
        ("退く", "どく", "to step aside / retreat", ["タイ"], ["しりぞ.く", "ど.く"]),
        ("退ける", "どける", "to move out of the way", ["タイ"], ["しりぞ.ける", "ど.ける"]),
        ("抱える", "かかえる", "to hold in arms / have", ["ホウ"], ["かか.える"]),
    ],
    # Lesson 201[cite: 28]
    [
        ("退院", "たいいん", "leaving hospital", ["タイイン"], []),
        ("退学", "たいがく", "dropping out of school", ["タイガク"], []),
        ("早退", "そうたい", "leaving early", ["ソウタイ"], []),
        ("引退", "いんたい", "retirement", ["インタイ"], []),
    ],
    # Lesson 202[cite: 28]
    [
        ("費", "ひ", "cost / expense", ["ヒ"], ["つい.やす"]),
        ("会費", "かいひ", "membership fee", ["カイヒ"], []),
        ("学費", "がくひ", "tuition / school expenses", ["ガクヒ"], []),
        ("費用", "ひよう", "cost / expense", ["ヒヨウ"], []),
    ],
    # Lesson 203[cite: 28]
    [
        ("生活費", "せいかつひ", "living expenses", ["セイカツヒ"], []),
        ("光熱費", "こうねつひ", "utility costs", ["コウネツヒ"], []),
        ("交際費", "こうさいひ", "entertainment expenses", ["コウサイヒ"], []),
        ("交通費", "こうつうひ", "transportation expenses", ["コウツウヒ"], []),
    ],
    # Lesson 204[cite: 28]
    [
        ("非", "ひ", "mistake / non- / un-", ["ヒ"], []),
        ("非常", "ひじょう", "emergency / extraordinary", ["ヒジョウ"], []),
        ("非常口", "ひじょうぐち", "emergency exit", ["ヒジョウグチ"], []),
        ("非常時", "ひじょうじ", "emergency", ["ヒジョウジ"], []),
    ],
    # Lesson 205[cite: 28]
    [
        ("非日常", "ひにちじょう", "extraordinary / out of the ordinary", ["ヒニチジョウ"], []),
        ("非公開", "ひこうかい", "closed to the public / private", ["ヒコウカイ"], []),
        ("非公式", "ひこうしき", "unofficial / informal", ["ヒコウシキ"], []),
        ("非常識", "ひじょうしき", "lack of common sense", ["ヒジョウシキ"], []),
    ],
    # Lesson 206[cite: 28]
    [
        ("喜ぶ", "よろこぶ", "to be delighted / glad", ["キ"], ["よろこ.ぶ"]),
        ("娘", "むすめ", "daughter / girl", [], ["むすめ"]),
        ("一人娘", "ひとりむすめ", "only daughter", [], ["ひとりむすめ"]),
        ("逃げる", "にげる", "to escape / run away", ["トウ"], ["に.げる", "に.がす"]),
        ("探る", "さぐる", "to search / probe", ["タン"], ["さぐ.る", "さが.す"]),
    ],
    # Lesson 207[cite: 28]
    [
        ("探す", "さがす", "to search for / look for", ["タン"], ["さが.す"]),
        ("犯す", "おかす", "to commit (a crime)", ["ハン"], ["おか.す"]),
        ("犯人", "はんにん", "criminal / culprit", ["ハンニン"], []),
        ("薬", "くすり", "medicine / drug", ["ヤク"], ["くすり"]),
        ("薬物", "やくぶつ", "medicines / drugs", ["ヤクブツ"], []),
    ],
    # Lesson 208[cite: 28]
    [
        ("うがい薬", "うがいぐすり", "gargle medicine", [], ["うがいぐすり"]),
        ("園", "その", "garden / park", ["エン"], ["その"]),
        ("公園", "こうえん", "public park", ["コウエン"], []),
        ("動物園", "どうぶつえん", "zoo", ["ドウブツエン"], []),
        ("戦犯", "せんぱん", "war criminal", ["センパン"], []),
    ],
    # Lesson 209[cite: 28]
    [
        ("疑い", "うたがい", "doubt / suspicion", ["ギ"], ["うたが.い"]),
        ("疑う", "うたがう", "to doubt / suspect", ["ギ"], ["うたが.う"]),
        ("疑問", "ぎもん", "question / doubt", ["ギモン"], []),
        ("緒", "しょ", "beginning / cord / together", ["ショ", "チョ"], ["お"]),
    ],
    # Lesson 210[cite: 28]
    [
        ("内緒", "ないしょ", "secret / confidentiality", ["ナイショ"], []),
        ("一緒", "いっしょ", "together", ["イッショ"], []),
        ("静か", "しずか", "quiet / peaceful", ["セイ", "ジョウ"], ["しず.か"]),
        ("具える", "そなえる", "to be furnished with", ["グ"], ["そな.える"]),
    ],
    # Lesson 211[cite: 28]
    [
        ("家具", "かぐ", "furniture", ["カグ"], []),
        ("道具", "どうぐ", "tool / instrument", ["ドウグ"], []),
        ("具合", "ぐあい", "condition / state / health", ["グアイ"], []),
        ("具体的", "ぐたいてき", "concrete / specific", ["グタイテキ"], []),
    ],
    # Lesson 212[cite: 28]
    [
        ("席", "せき", "seat", ["セキ"], []),
        ("満席", "まんせき", "full house / all seats occupied", ["マンセキ"], []),
        ("座席", "ざせき", "seat", ["ザセキ"], []),
        ("出席", "しゅっせき", "attendance / presence", ["シュッセキ"], []),
    ],
    # Lesson 213[cite: 28]
    [
        ("欠席", "けっせき", "absence", ["ケッセキ"], []),
        ("指定席", "していせき", "reserved seat", ["シテイセキ"], []),
        ("自由席", "じゆうせき", "unreserved seat", ["ジユウセキ"], []),
        ("優先席", "ゆうせんせき", "priority seat", ["ユウセンセキ"], []),
    ],
    # Lesson 214[cite: 28]
    [
        ("助手席", "じょしゅせき", "front passenger seat", ["ジョシュセキ"], []),
        ("運転席", "うんてんせき", "driver's seat", ["ウンテンセキ"], []),
        ("速い", "はやい", "fast / quick", ["ソク"], ["はや.い", "すみ.やか"]),
        ("速度", "そくど", "speed / velocity", ["ソクド"], []),
        ("速やか", "すみやか", "prompt / speedy", ["ソク"], ["すみ.やか"]),
    ],
    # Lesson 215[cite: 28]
    [
        ("早速", "さっそく", "at once / immediately", ["サッソク"], []),
        ("高速道路", "こうそくどうろ", "expressway / highway", ["コウソクドウロ"], []),
        ("舞う", "まう", "to dance / flutter", ["ブ"], ["ま.う", "まい"]),
        ("お見舞い", "おみまい", "visiting someone who is ill", [], ["おみまい"]),
    ],
    # Lesson 216[cite: 28]
    [
        ("宿", "やど", "inn / lodging", ["シュク"], ["やど", "やど.る"]),
        ("宿題", "しゅくだい", "homework", ["シュクダイ"], []),
        ("新宿", "しんじゅく", "Shinjuku", ["シンジュク"], []),
        ("程", "ほど", "extent / degree", ["テイ"], ["ほど"]),
        ("程度", "ていど", "degree / amount / level", ["テイド"], []),
    ],
    # Lesson 217[cite: 28]
    [
        ("日程", "にってい", "schedule / itinerary", ["ニッテイ"], []),
        ("倒す", "たおす", "to knock down / defeat", ["トウ"], ["たお.す", "たお.れる"]),
        ("倒れる", "たおれる", "to collapse / fall down", ["トウ"], ["たお.れる"]),
        ("倒産", "とうさん", "bankruptcy", ["トウサン"], []),
    ],
    # Lesson 218[cite: 28]
    [
        ("面倒", "めんどう", "trouble / difficulty / care", ["メンドウ"], []),
        ("寝る", "ねる", "to sleep / go to bed", ["シン"], ["ね.る", "ね.かす"]),
        ("昼寝", "ひるね", "afternoon nap", [], ["ひるね"]),
        ("寝不足", "ねぶそく", "lack of sleep", ["ネブソク"], []),
    ],
    # Lesson 219[cite: 28]
    [
        ("お宅", "おたく", "your house / home (polite)", ["タク"], []),
        ("自宅", "じたく", "one's own home", ["ジタク"], []),
        ("絵", "え", "picture / drawing / painting", ["カイ", "エ"], []),
        ("絵画", "かいが", "painting / picture", ["カイガ"], []),
    ],
    # Lesson 220[cite: 28]
    [
        ("破る", "やぶる", "to tear / break / defeat", ["ハ"], ["やぶ.る", "やぶ.れる"]),
        ("破れる", "やぶれる", "to get torn / be defeated", ["ハ"], ["やぶ.れる"]),
        ("庭", "にわ", "garden / yard", ["テイ"], ["にわ"]),
        ("婦", "ふ", "woman / wife", ["フ"], []),
        ("家庭", "かてい", "home / family / household", ["カテイ"], []),
    ],
    # Lesson 221[cite: 29]
    [
        ("夫婦", "ふうふ", "married couple / spouses", ["フウフ"], []),
        ("主婦", "しゅふ", "housewife / homemaker", ["シュフ"], []),
        ("婦人服", "ふじんふく", "women's clothing", ["フジンフク"], []),
        ("余る", "あまる", "to remain / be left over", ["ヨ"], ["あま.る", "あま.す"]),
        ("余り", "あまり", "remainder / not very", ["ヨ"], ["あま.り"]),
    ],
    # Lesson 222[cite: 29]
    [
        ("訪ねる", "たずねる", "to visit / call on", ["ホウ"], ["たず.ねる", "おとず.れる"]),
        ("訪問", "ほうもん", "call / visit", ["ホウモン"], []),
        ("訪日", "ほうにち", "visit to Japan", ["ホウニチ"], []),
        ("冷たい", "つめたい", "cold (to the touch)", ["レイ"], ["つめ.たい", "ひ.える"]),
        ("冷静", "れいせい", "calm / cool-headed", ["レイセイ"], []),
    ],
    # Lesson 223[cite: 29]
    [
        ("冷える", "ひえる", "to grow cold / chill", ["レイ"], ["ひ.える"]),
        ("冷やす", "ひやす", "to cool / chill", ["レイ"], ["ひ.やす"]),
        ("冷夏", "れいか", "cool summer", ["レイカ"], []),
        ("暮らす", "くらす", "to live / make a living", ["ボ"], ["くら.す", "く.れる"]),
    ],
    # Lesson 224[cite: 29]
    [
        ("暮れる", "くれる", "to get dark / come to an end", ["ボ"], ["く.れる"]),
        ("年の暮れ", "としのくれ", "end of the year", [], ["としのくれ"]),
        ("一人暮らし", "ひとりぐらし", "living alone", [], ["ひとりぐらし"]),
        ("お腹", "おなか", "stomach / belly", ["フク"], ["はら"]),
    ],
    # Lesson 225[cite: 29]
    [
        ("腹が立つ", "はらがたつ", "to get angry", [], ["はらがた.つ"]),
        ("お腹が空く", "おなかがすく", "to get hungry", [], ["おなかがす.く"]),
        ("危ない", "あぶない", "dangerous / risky", ["キ"], ["あぶ.ない", "あや.うい"]),
        ("許す", "ゆるす", "to permit / forgive", ["キョ"], ["ゆる.す"]),
    ],
    # Lesson 226[cite: 29]
    [
        ("許可", "きょか", "permission / approval", ["キョカ"], []),
        ("無許可", "むきょか", "without permission", ["ムキョカ"], []),
        ("似る", "にる", "to resemble / look like", ["ジ"], ["に.る"]),
        ("真似", "まね", "imitation / mimicry", [], ["まね"]),
    ],
    # Lesson 227[cite: 29]
    [
        ("似合う", "にあう", "to suit / match well", [], ["にあ.う"]),
        ("険しい", "けわしい", "steep / grim / severe", ["ケン"], ["けわ.しい"]),
        ("危険", "きけん", "danger / peril / hazard", ["キケン"], []),
        ("財", "ざい", "wealth / property / assets", ["ザイ", "サイ"], []),
    ],
    # Lesson 228[cite: 29]
    [
        ("財産", "ざいさん", "property / fortune / assets", ["ザイサン"], []),
        ("遊ぶ", "あそぶ", "to play / enjoy oneself", ["ユウ", "ユ"], ["あそ.ぶ"]),
        ("遊園地", "ゆうえんち", "amusement park", ["ユウエンチ"], []),
        ("値", "あたい", "value / price / worth", ["チ"], ["ね", "あたい"]),
    ],
    # Lesson 229[cite: 29]
    [
        ("恐ろしい", "おそろしい", "terrible / dreadful", ["キョウ"], ["おそ.ろしい"]),
        ("値", "ね", "price / cost", ["チ"], ["ね"]),
        ("値段", "ねだん", "price / cost", ["ネダン"], []),
        ("暗い", "くらい", "dark / gloomy", ["アン"], ["くら.い"]),
    ],
    # Lesson 230[cite: 29]
    [
        ("暗記", "あんき", "memorization", ["アンキ"], []),
        ("積む", "つむ", "to pile up / stack / load", ["セキ"], ["つ.む", "つ.もる"]),
        ("積もる", "つもる", "to pile up / accumulate", ["セキ"], ["つ.もる"]),
        ("夢", "ゆめ", "dream", ["ム"], ["ゆめ"]),
    ],
    # Lesson 231[cite: 29]
    [
        ("夢中", "むちゅう", "absorbed in / crazy about", ["ムチュウ"], []),
        ("痛み", "いたみ", "pain / ache", ["ツウ"], ["いた.み"]),
        ("痛い", "いたい", "painful / sore", ["ツウ"], ["いた.い"]),
        ("頭痛", "ずつう", "headache", ["ズツウ"], []),
    ],
    # Lesson 232[cite: 29]
    [
        ("腹痛", "ふくつう", "stomachache", ["フクツウ"], []),
        ("頭が痛い", "あたまがいたい", "to have a headache", [], ["あたまがいた.い"]),
        ("富", "とみ", "wealth / riches", ["フ", "フウ"], ["と.む", "とみ"]),
        ("刻む", "きざむ", "to mince / carve / engrave", ["コク"], ["きざ.む"]),
    ],
    # Lesson 233[cite: 29]
    [
        ("時刻", "じこく", "time / hour", ["ジコク"], []),
        ("時刻表", "じこくひょう", "timetable / schedule", ["ジコクヒョウ"], []),
        ("鳴る", "なる", "to sound / ring", ["メイ"], ["な.る", "な.く"]),
        ("鳴く", "なく", "to cry / chirp / bark (animal)", ["メイ"], ["な.く"]),
    ],
    # Lesson 234[cite: 29]
    [
        ("欲しい", "ほしい", "wanted / desired", ["ヨク"], ["ほ.しい"]),
        ("食欲", "しょくよく", "appetite", ["ショクヨク"], []),
        ("途", "と", "way / route", ["ト"], []),
        ("途中", "とちゅう", "on the way / halfway", ["トチュウ"], []),
        ("欲求", "よっきゅう", "desire / urge / want", ["ヨッキュウ"], []),
    ],
    # Lesson 235[cite: 29]
    [
        ("途中下車", "とちゅうげしゃ", "stopping over (on a train trip)", ["トチュウゲシャ"], []),
        ("曲", "きょく", "musical piece / tune / curve", ["キョク"], ["ま.がる", "ま.げる"]),
        ("曲がる", "まがる", "to bend / turn", ["キョク"], ["ま.がる"]),
        ("完ぺき", "かんぺき", "perfection / flawless", ["カンペキ"], []),
    ],
    # Lesson 236[cite: 29]
    [
        ("不完全", "ふかんぜん", "imperfect / incomplete", ["フカンゼン"], []),
        ("願い", "ねがい", "desire / wish / request", ["ガン"], ["ねが.い"]),
        ("願う", "ねがう", "to desire / wish / hope", ["ガン"], ["ねが.う"]),
        ("お願いします", "おねがいします", "please", [], ["おねがいします"]),
        ("出願", "しゅつがん", "application", ["シュツガン"], []),
    ],
    # Lesson 237[cite: 29]
    [
        ("罪", "つみ", "crime / sin / guilt", ["ザイ"], ["つみ"]),
        ("犯罪", "はんざい", "crime / offense", ["ハンザイ"], []),
        ("陽", "よう", "sunshine / positive", ["ヨウ"], ["ひ"]),
        ("太陽", "たいよう", "the sun", ["タイヨウ"], []),
    ],
    # Lesson 238[cite: 29]
    [
        ("散る", "ちる", "to fall / scatter (blossoms)", ["サン"], ["ち.る", "ち.らす"]),
        ("散らかる", "ちらかる", "to be in disorder / scattered", ["サン"], ["ち.らかる"]),
        ("散らかす", "ちらかす", "to scatter around / mess up", ["サン"], ["ち.らかす"]),
        ("散歩", "さんぽ", "walk / stroll", ["サンポ"], []),
    ],
    # Lesson 239[cite: 29]
    [
        ("解散", "かいさん", "breakup / dissolution", ["カイサン"], []),
        ("掛かる", "かかる", "to take (time/money) / hang", [], ["か.かる", "か.ける"]),
        ("掛ける", "かける", "to hang / make (a call)", [], ["か.ける"]),
        ("昨", "さく", "yesterday / previous", ["サク"], []),
        ("昨今", "さっこん", "nowadays / recently", ["サッコン"], []),
    ],
    # Lesson 240[cite: 29]
    [
        ("昨年", "さくねん", "last year", ["サクネン"], []),
        ("昨日", "きのう", "yesterday", ["サクジツ"], ["きのう"]),
        ("一昨年", "おととし", "year before last", [], ["おととし"]),
        ("一昨日", "おととい", "day before yesterday", [], ["おととい"]),
    ],
    # Lesson 241[cite: 30]
    [
        ("怒る", "おこる", "to get angry", ["ド"], ["おこ.る", "いか.る"]),
        ("留める", "とめる", "to fasten / stop / detain", ["リュウ", "ル"], ["と.める", "と.まる"]),
        ("留学", "りゅうがく", "studying abroad", ["リュウガク"], []),
        ("留守", "るす", "absence / being away from home", ["ルス"], []),
    ],
    # Lesson 242[cite: 30]
    [
        ("留学生", "りゅうがくせい", "international student", ["リュウガクセイ"], []),
        ("留守番電話", "るすばんでんわ", "answering machine", ["ルスバンデンワ"], []),
        ("列", "れつ", "queue / line / row", ["レツ"], []),
        ("行列", "ぎょうれつ", "line / queue / procession", ["ギョウレツ"], []),
        ("列車", "れっしゃ", "train", ["レッシャ"], []),
    ],
    # Lesson 243[cite: 30]
    [
        ("雪", "ゆき", "snow", ["セツ"], ["ゆき"]),
        ("払う", "はらう", "to pay / clear away", [], ["はら.う"]),
        ("支払い", "しはらい", "payment", [], ["しはらい"]),
        ("支払う", "しはらう", "to pay", [], ["しはら.う"]),
    ],
    # Lesson 244[cite: 30]
    [
        ("払い戻し", "はらいもどし", "refund / repayment", [], ["はらいもどし"]),
        ("払い戻す", "はらいもどす", "to refund / pay back", [], ["はらいもど.す"]),
        ("給", "きゅう", "salary / supply", ["キュウ"], []),
        ("給料", "きゅうりょう", "salary / wages", ["キュウリョウ"], []),
    ],
    # Lesson 245[cite: 30]
    [
        ("時給", "じきゅう", "hourly wage", ["ジキュウ"], []),
        ("給食", "きゅうしょく", "school lunch", ["キュウショク"], []),
        ("敗", "はい", "defeat / failure", ["ハイ"], ["やぶ.れる"]),
        ("失敗", "しっぱい", "failure / blunder", ["シッパイ"], []),
    ],
    # Lesson 246[cite: 30]
    [
        ("捕まる", "つかまる", "to be caught / arrested", ["ホ"], ["つか.まる", "つか.まえる"]),
        ("捕まえる", "つかまえる", "to catch / arrest", ["ホ"], ["つか.まえる"]),
        ("忘れる", "わすれる", "to forget", ["ボウ"], ["わす.れる"]),
        ("忘れ物", "わすれもの", "lost article / thing forgotten", [], ["わすれもの"]),
    ],
    # Lesson 247[cite: 30]
    [
        ("忘年会", "ぼうねんかい", "year-end party", ["ボウネンカイ"], []),
        ("晴れる", "はれる", "to clear up (weather)", ["セイ"], ["は.れる", "は.らす"]),
        ("困る", "こまる", "to be troubled / in difficulty", ["コン"], ["こま.る"]),
        ("原因", "げんいん", "cause / origin / source", ["ゲンイン"], []),
        ("因果", "いんが", "cause and effect / karma", ["インガ"], []),
    ],
    # Lesson 248[cite: 30]
    [
        ("折る", "おる", "to break / fold / bend", ["セツ"], ["お.る", "お.れる"]),
        ("折れる", "おれる", "to break / be folded", ["セツ"], ["お.れる"]),
        ("迎える", "むかえる", "to go out to meet / welcome", ["ゲイ"], ["むか.える"]),
        ("出迎え", "でむかえ", "meeting / reception", [], ["でむかえ"]),
        ("折", "おり", "occasion / opportunity / fold", ["セツ"], ["おり"]),
    ],
    # Lesson 249[cite: 30]
    [
        ("出迎える", "でむかえる", "to meet / greet", [], ["でむか.える"]),
        ("悲しみ", "かなしみ", "sadness / sorrow", ["ヒ"], ["かな.しみ"]),
        ("悲しい", "かなしい", "sad / sorrowful", ["ヒ"], ["かな.しい"]),
        ("悲しむ", "かなしむ", "to be sad / mourn", ["ヒ"], ["かな.しむ"]),
    ],
    # Lesson 250[cite: 30]
    [
        ("港", "みなと", "harbor / port", ["コウ"], ["みなと"]),
        ("空港", "くうこう", "airport", ["クウコウ"], []),
        ("責める", "せめる", "to condemn / blame", ["セキ"], ["せ.める"]),
        ("責任", "せきにん", "responsibility", ["セキニン"], []),
    ],
    # Lesson 251[cite: 31]
    [
        ("無責任", "むせきにん", "irresponsibility", ["ムセキニン"], []),
        ("除く", "のぞく", "to remove / exclude", ["ジョ", "ジ"], ["のぞ.く"]),
        ("困る", "こまる", "to be bothered / troubled", ["コン"], ["こま.る"]),
        ("閉まる", "しまる", "to close / be shut", ["ヘイ"], ["し.まる", "し.める"]),
        ("困難", "こんなん", "difficulty / hardship", ["コンナン"], []),
    ],
    # Lesson 252[cite: 31]
    [
        ("閉める", "しめる", "to close / shut", ["ヘイ"], ["し.める"]),
        ("閉じる", "とじる", "to close / shut (book/eyes)", ["ヘイ"], ["と.じる", "と.ざす"]),
        ("吸う", "すう", "to breathe in / smoke / suck", ["キュウ"], ["す.う"]),
        ("髪", "かみ", "hair", ["ハツ"], ["かみ"]),
        ("呼吸", "こきゅう", "breathing / respiration", ["コキュウ"], []),
    ],
    # Lesson 253[cite: 31]
    [
        ("髪をとかす", "かみをとかす", "to comb one's hair", [], ["かみをとか.す"]),
        ("白髪", "しらが", "white/gray hair", ["ハクハツ"], ["しらが"]),
        ("束", "たば", "bundle / bunch", ["ソク"], ["たば"]),
        ("約束", "やくそく", "promise / appointment", ["ヤクソク"], []),
    ],
    # Lesson 254[cite: 31]
    [
        ("眠り", "ねむり", "sleep", ["ミン"], ["ねむ.り"]),
        ("眠い", "ねむい", "sleepy / drowsy", ["ミン"], ["ねむ.い"]),
        ("眠る", "ねむる", "to sleep", ["ミン"], ["ねむ.る"]),
        ("居眠り", "いねむり", "dozing / nodding off", [], ["いねむり"]),
    ],
    # Lesson 255[cite: 31]
    [
        ("易しい", "やさしい", "easy / plain / simple", ["イ", "エキ"], ["やさ.しい"]),
        ("容易", "ようい", "easy / simple", ["ヨウイ"], []),
        ("窓", "まど", "window", ["ソウ"], ["まど"]),
        ("窓口", "まどぐち", "ticket window / counter", [], ["まどぐち"]),
    ],
    # Lesson 256[cite: 31]
    [
        ("窓側", "まどがわ", "window seat / window side", [], ["まどがわ"]),
        ("祖", "そ", "ancestor / founder", ["ソ"], []),
        ("祖父", "そふ", "grandfather", ["ソフ"], []),
        ("祖母", "そぼ", "grandmother", ["ソボ"], []),
    ],
    # Lesson 257[cite: 31]
    [
        ("先祖", "せんぞ", "ancestor", ["センゾ"], []),
        ("祖先", "そせん", "ancestor", ["ソセン"], []),
        ("勤め", "つとめ", "service / duty / job", ["キン", "ゴン"], ["つと.め"]),
        ("勤める", "つとめる", "to work (for) / be employed", ["キン"], ["つと.める"]),
    ],
    # Lesson 258[cite: 31]
    [
        ("転勤", "てんきん", "job transfer", ["テンキン"], []),
        ("通勤", "つうきん", "commuting to work", ["ツウキン"], []),
        ("勤務", "きんむ", "service / duty / work", ["キンム"], []),
        ("昔", "むかし", "olden days / former times", ["セキ", "シャク"], ["むかし"]),
    ],
    # Lesson 259[cite: 31]
    [
        ("便", "びん", "flight / mail / service", ["ベン", "ビン"], ["たよ.り"]),
        ("便り", "たより", "news / tidings / letter", ["ビン"], ["たよ.り"]),
        ("船便", "ふなびん", "surface mail / sea mail", ["センビン"], ["ふなびん"]),
        ("便利", "べんり", "convenient / handy", ["ベンリ"], []),
    ],
    # Lesson 260[cite: 31]
    [
        ("不便", "ふべん", "inconvenience", ["フベン"], []),
        ("宅配便", "たくはいびん", "home delivery service", ["タクハイビン"], []),
        ("適する", "てきする", "to fit / suit", ["テキ"], ["てき.する"]),
        ("適当", "てきとう", "suitable / appropriate", ["テキトウ"], []),
    ],
    # Lesson 261[cite: 31]
    [
        ("吹く", "ふく", "to blow (wind)", ["スイ"], ["ふ.く"]),
        ("候", "こう", "climate / season / weather", ["コウ"], ["そうろう"]),
        ("天候", "てんこう", "weather", ["テンコウ"], []),
        ("気候", "きこう", "climate", ["キコウ"], []),
    ],
    # Lesson 262[cite: 31]
    [
        ("怖い", "こわい", "scary / frightening", ["フ"], ["こわ.い"]),
        ("恐怖", "きょうふ", "fear / dread / terror", ["キョウフ"], []),
        ("恐怖心", "きょうふしん", "sense of fear", ["キョウフシン"], []),
        ("恐怖映画", "きょうふえいが", "horror movie", ["キョウフエイガ"], []),
    ],
    # Lesson 263[cite: 31]
    [
        ("辞める", "やめる", "to resign / quit", ["ジ"], ["や.める"]),
        ("辞書", "じしょ", "dictionary", ["ジショ"], []),
        ("否", "いな", "no / negation", ["ヒ"], ["いな"]),
        ("否定", "ひてい", "denial / negation", ["ヒテイ"], []),
    ],
    # Lesson 264[cite: 31]
    [
        ("遅め", "おそめ", "somewhat late", ["チ"], ["おそ.め"]),
        ("遅い", "おそい", "slow / late", ["チ"], ["おく.れる", "おそ.い"]),
        ("遅れる", "おくれる", "to be late / delayed", ["チ"], ["おく.れる"]),
        ("遅刻", "ちこく", "tardiness / being late", ["チコク"], []),
    ],
    # Lesson 265[cite: 31]
    [
        ("乗り遅れる", "のりおくれる", "to miss (a train/bus)", [], ["のりおく.れる"]),
        ("煙", "けむり", "smoke / fumes", ["エン"], ["けむ.る", "けむり"]),
        ("徒", "と", "follower / on foot", ["ト"], []),
        ("生徒", "せいと", "pupil / student", ["セイト"], []),
        ("徒然", "つれづれ", "tedium / boredom", ["トゼン"], ["つれづれ"]),
    ],
    # Lesson 266[cite: 31]
    [
        ("徒歩", "とほ", "walking / on foot", ["トホ"], []),
        ("迷い", "まよい", "hesitation / bewilderment", ["メイ"], ["まよ.い"]),
        ("迷う", "まよう", "to lose one's way / hesitate", ["メイ"], ["まよ.う"]),
        ("迷子", "まいご", "lost child", ["マイゴ"], []),
        ("煙草", "たばこ", "tobacco / cigarette", [], ["たばこ"]),
    ],
    # Lesson 267[cite: 31]
    [
        ("洗う", "あらう", "to wash", ["セン"], ["あら.う"]),
        ("手洗い", "てあらい", "restroom / washing hands", [], ["てあらい"]),
        ("お手洗い", "おてあらい", "restroom / lavatory", [], ["おてあらい"]),
        ("互いに", "たがいに", "mutually / with each other", ["ゴ"], ["たが.いに"]),
    ],
    # Lesson 268[cite: 31]
    [
        ("才", "さい", "talent / ability / years old", ["サイ"], []),
        ("才能", "さいのう", "talent / ability", ["サイノウ"], []),
        ("天才", "てんさい", "genius", ["テンサイ"], []),
        ("更に", "さらに", "furthermore / again", ["コウ"], ["さら.に"]),
    ],
    # Lesson 269[cite: 31]
    [
        ("変更", "へんこう", "change / modification", ["ヘンコウ"], []),
        ("歯", "は", "tooth / teeth", ["シ"], ["は"]),
        ("歯科医", "しかい", "dentist", ["シカイ"], []),
        ("歯医者", "はいしゃ", "dentist", [], ["はいしゃ"]),
    ],
    # Lesson 270[cite: 31]
    [
        ("盗む", "ぬすむ", "to steal", ["トウ"], ["ぬす.む"]),
        ("慣れる", "なれる", "to get used to", ["カン"], ["な.れる", "な.らす"]),
        ("習慣", "しゅうかん", "habit / custom", ["シュウカン"], []),
        ("晩", "ばん", "evening / night", ["バン"], []),
    ],
    # Lesson 271[cite: 31]
    [
        ("毎晩", "まいばん", "every night", ["マイバン"], []),
        ("今晩", "こんばん", "tonight / this evening", ["コンバン"], []),
        ("晩ご飯", "ばんごはん", "dinner / supper", ["バンゴハン"], []),
        ("箱", "はこ", "box / case", ["ソウ"], ["はこ"]),
    ],
    # Lesson 272[cite: 32]
    [
        ("到", "とう", "arrival / reach", ["トウ"], []),
        ("到着", "とうちゃく", "arrival", ["トウチャク"], []),
        ("頂く", "いただく", "to receive / eat (humble)", ["チョウ"], ["いただ.く"]),
        ("頂上", "ちょうじょう", "summit / top / peak", ["チョウジョウ"], []),
    ],
    # Lesson 273[cite: 32]
    [
        ("杯", "はい", "cup / glass / counter", ["ハイ"], ["さかずき"]),
        ("六杯", "ろっぱい", "six cups/glasses", ["ロッパイ"], []),
        ("皆さん", "みなさん", "everyone / everybody", [], ["みなさん"]),
        ("招く", "まねく", "to invite / beckon", ["ショウ"], ["まね.く"]),
        ("皆", "みんな", "all / everyone", ["カイ"], ["みな", "みんな"]),
    ],
    # Lesson 274[cite: 32]
    [
        ("招待", "しょうたい", "invitation", ["ショウタイ"], []),
        ("寒い", "さむい", "cold (weather)", ["カン"], ["さむ.い"]),
        ("恥ずかしい", "はずかしい", "embarrassed / ashamed", ["チ"], ["は.ずかしい"]),
        ("疲れる", "つかれる", "to get tired / fatigued", ["ヒ"], ["つか.れる"]),
        ("皆無", "かいむ", "nonexistent / nil", ["カイム"], []),
    ],
    # Lesson 275[cite: 32]
    [
        ("貧しい", "まずしい", "poor / needy", ["ヒン", "ビン"], ["まず.しい"]),
        ("猫", "ねこ", "cat", ["ビョウ"], ["ねこ"]),
        ("誤り", "あやまり", "error / mistake", ["ゴ"], ["あやま.り"]),
        ("誤解", "ごかい", "misunderstanding", ["ゴカイ"], []),
    ],
    # Lesson 276[cite: 32]
    [
        ("努める", "つとめる", "to endeavor / try hard", ["ド"], ["つと.める"]),
        ("努力", "どりょく", "effort / exertion", ["ドリョク"], []),
        ("幾ら", "いくら", "how much", ["キ"], ["いく.ら"]),
        ("幾つ", "いくつ", "how many / how old", ["キ"], ["いく.つ"]),
    ],
    # Lesson 277[cite: 32]
    [
        ("賛", "さん", "approve / praise", ["サン"], []),
        ("賛成", "さんせい", "approval / agreement", ["サンセイ"], []),
        ("偶に", "たまに", "occasionally / once in a while", ["グウ"], ["たま.に"]),
        ("偶然", "ぐうぜん", "by chance / unexpectedly", ["グウゼン"], []),
    ],
    # Lesson 278[cite: 32]
    [
        ("泳ぐ", "およぐ", "to swim", ["エイ"], ["およ.ぐ"]),
        ("水泳", "すいえい", "swimming", ["スイエイ"], []),
        ("靴", "くつ", "shoes / footwear", ["カ"], ["くつ"]),
        ("靴下", "くつした", "socks", [], ["くつした"]),
    ],
    # Lesson 279[cite: 32]
    [
        ("偉い", "えらい", "great / admirable / famous", ["イ"], ["えら.い"]),
        ("偉大", "いだい", "greatness / mighty", ["イダイ"], []),
        ("口げんか", "くちげんか", "quarrel / verbal dispute", [], ["くちげんか"]),
        ("話しかける", "はなしかける", "to speak to / address", [], ["はなしか.ける"]),
    ],
    # Lesson 280[cite: 32]
    [
        ("本人", "ほんにん", "the person himself/herself", ["ホンニン"], []),
        ("目にする", "めにする", "to see / catch sight of", [], ["めにす.る"]),
        ("見下ろす", "みおろす", "to look down on / overlook", [], ["みおろ.す"]),
        ("生える", "はえる", "to grow / sprout", ["セイ"], ["は.える"]),
    ],
    # Lesson 281[cite: 32]
    [
        ("名字", "みょうじ", "surname / family name", ["ミョウジ"], []),
        ("本日", "ほんじつ", "today / this day", ["ホンジツ"], []),
        ("上品", "じょうひん", "elegant / refined", ["ジョウヒン"], []),
        ("古着", "ふるぎ", "used clothing / secondhand clothes", [], ["ふるぎ"]),
    ],
    # Lesson 282[cite: 32]
    [
        ("真っ赤", "まっか", "bright red / deep red", ["マッカ"], []),
        ("元", "げん", "origin / energy", ["ゲン", "ガン"], ["もと"]),
        ("生き生き", "いきいき", "vividly / lively", [], ["いきいき"]),
        ("休学", "きゅうがく", "temporary absence from school", ["キュウガク"], []),
    ],
    # Lesson 283[cite: 32]
    [
        ("通行止め", "つうこうどめ", "road closed", ["ツウコウドメ"], []),
        ("借金", "しゃっきん", "debt / loan", ["シャッキン"], []),
        ("特売日", "とくばいび", "special sale day", ["トクバイビ"], []),
        ("住まい", "すまい", "dwelling / residence", ["ジュウ"], ["す.まい"]),
    ],
    # Lesson 284[cite: 32]
    [
        ("問う", "とう", "to ask / question", ["モン"], ["と.う", "と.い"]),
        ("外見", "がいけん", "outward appearance", ["ガイケン"], []),
        ("切らす", "きらす", "to run out of", ["セツ"], ["き.らす"]),
        ("真夜中", "まよなか", "dead of night / midnight", [], ["まよなか"]),
    ],
    # Lesson 285[cite: 32]
    [
        ("運動会", "うんどうかい", "sports day / athletic meet", ["ウンドウカイ"], []),
        ("新発売", "しんはつばい", "newly released / on sale", ["シンハツバイ"], []),
        ("出入り口", "でいりぐち", "exit and entrance", [], ["でいりぐち"]),
        ("学者", "がくしゃ", "scholar / academic", ["ガクシャ"], []),
    ],
    # Lesson 286[cite: 32]
    [
        ("昼食", "ちゅうしょく", "lunch", ["チュウショク"], []),
        ("前日", "ぜんじつ", "the previous day", ["ゼンジツ"], []),
        ("行き先", "いきさき", "destination", [], ["いきさき"]),
        ("国立", "こくりつ", "national", ["コクリツ"], []),
    ],
    # Lesson 287[cite: 32]
    [
        ("真冬日", "まふゆび", "freezing day (below 0°C)", [], ["まふゆび"]),
        ("発売", "はつばい", "sale / release", ["ハツバイ"], []),
        ("気になる", "きになる", "to be on one's mind / worry", [], ["きにな.る"]),
        ("本音", "ほんね", "true intention / real feelings", ["ホンネ"], []),
    ],
    # Lesson 288[cite: 32]
    [
        ("工事", "こうじ", "construction work", ["コウジ"], []),
        ("正社員", "せいしゃいん", "regular full-time employee", ["セイシャイン"], []),
        ("母親", "ははおや", "mother", [], ["ははおや"]),
        ("代わり", "かわり", "substitute / replacement", ["ダイ"], ["か.わり"]),
    ],
    # Lesson 289[cite: 33]
    [
        ("意外", "いがい", "unexpected / surprising", ["イガイ"], []),
        ("入館料", "にゅうかんりょう", "admission fee (museum/library)", ["ニュウカンリョウ"], []),
        ("赤道", "せきどう", "equator", ["セキドウ"], []),
        ("やる気", "やるき", "motivation / willingness", [], ["やるき"]),
    ],
    # Lesson 290[cite: 33]
    [
        ("物語", "ものがたり", "tale / story / legend", [], ["ものがたり"]),
        ("立ち上がる", "たちあがる", "to stand up / rise", [], ["たちあ.がる"]),
        ("無地", "むじ", "plain / solid color (fabric)", ["ムジ"], []),
        ("でき上がる", "できあがる", "to be completed / ready", [], ["できあ.がる"]),
    ],
    # Lesson 291[cite: 33]
    [
        ("特色", "とくしょく", "characteristic / feature", ["トクショク"], []),
        ("無事", "ぶじ", "safety / peace / without incident", ["ブジ"], []),
        ("朝食", "ちょうしょく", "breakfast", ["チョウショク"], []),
        ("品物", "しなもの", "goods / article / item", [], ["しなもの"]),
    ],
    # Lesson 292[cite: 33]
    [
        ("家電", "かでん", "home appliances", ["カデン"], []),
        ("強風", "きょうふう", "strong wind / gale", ["キョウフウ"], []),
        ("一人ひとり", "ひとりひとり", "one by one / each person", [], ["ひとりひとり"]),
    ],
    # Lesson 293[cite: 33]
    [
        ("空き地", "あきち", "vacant lot", [], ["あきち"]),
        ("金持ち", "かねもち", "rich person", [], ["かねもち"]),
        ("自習", "じしゅう", "self-study", ["ジシュウ"], []),
        ("使用料", "しようりょう", "usage fee / rental fee", ["シヨウリョウ"], []),
    ],
    # Lesson 294[cite: 33]
    [
        ("前半", "ぜんはん", "first half", ["ゼンハン"], []),
        ("味わう", "あじわう", "to taste / savor / appreciate", ["ミ"], ["あじ.わう"]),
        ("歌手", "かしゅ", "singer", ["カシュ"], []),
        ("通じる", "つうじる", "to be understood / lead to", ["ツウ"], ["つう.じる"]),
    ],
    # Lesson 295[cite: 33]
    [
        ("一度に", "いちどに", "all at once / at one time", ["イチド"], []),
        ("英会話", "えいかいわ", "English conversation", ["エイカイワ"], []),
        ("かっこ悪い", "かっこわるい", "unattractive / uncool", [], ["かっこわる.い"]),
        ("以前", "いぜん", "ago / since / before", ["イゼン"], []),
    ],
    # Lesson 296[cite: 33]
    [
        ("多め", "おおめ", "a bit more / generous amount", ["タ"], ["おお.め"]),
        ("出会い", "であい", "encounter / meeting", [], ["であい"]),
        ("味見", "あじみ", "tasting / sampling food", [], ["あじみ"]),
        ("耳にする", "みみにする", "to hear / learn of", [], ["みみにす.る"]),
    ],
    # Lesson 297[cite: 33]
    [
        ("気味が悪い", "きみがわるい", "creepy / eerie / unpleasant", [], ["きみがわる.い"]),
        ("あて先", "あてさき", "recipient's address", [], ["あてさき"]),
        ("立ち止まる", "たちどまる", "to stop / halt / stand still", [], ["たちど.まる"]),
        ("送金", "そうきん", "remittance / sending money", ["ソウキン"], []),
    ],
    # Lesson 298[cite: 33]
    [
        ("真っ白", "まっしろ", "pure white", ["マッシロ"], []),
        ("体重計", "たいじゅうけい", "bathroom scale", ["タイジュウケイ"], []),
        ("名作", "めいさく", "masterpiece", ["メイサク"], []),
        ("代金", "だいきん", "price / payment / charge", ["ダイキン"], []),
    ],
    # Lesson 299[cite: 33]
    [
        ("本気", "ほんき", "seriousness / earnestness", ["ホンキ"], []),
        ("生まれ", "うまれ", "birth / birthplace", ["セイ"], ["う.まれ"]),
        ("出品", "しゅっぴん", "exhibiting / listing for sale", ["シュッピン"], []),
        ("中心", "ちゅうしん", "center / core / heart", ["チュウシン"], []),
    ],
    # Lesson 300[cite: 33]
    [
        ("前後", "ぜんご", "front and back / around", ["ゼンゴ"], []),
        ("大さじ", "おおさじ", "tablespoon", [], ["おおさじ"]),
        ("空きびん", "あきびん", "empty bottle", [], ["あきびん"]),
        ("飲み会", "のみかい", "drinking party / get-together", [], ["のみかい"]),
    ],
    # Lesson 301[cite: 34]
    [
        ("悪口", "わるぐち", "slander / bad-mouthing", ["アッコウ"], ["わるぐち"]),
        ("お代わり", "おかわり", "second helping / refill", [], ["おかわり"]),
        ("日にち", "ひにち", "date / number of days", [], ["ひにち"]),
        ("下車", "げしゃ", "getting off a train/bus", ["ゲシャ"], []),
    ],
    # Lesson 302[cite: 34]
    [
        ("親しい", "したしい", "close / intimate / friendly", ["シン"], ["した.しい"]),
        ("にわか雨", "にわかあめ", "rain shower", [], ["にわかあめ"]),
        ("新車", "しんしゃ", "new car", ["シンシャ"], []),
        ("冬日", "ふゆび", "winter day (below 0°C low)", [], ["ふゆび"]),
    ],
    # Lesson 303[cite: 34]
    [
        ("社会的", "しゃかいてき", "social", ["シャカイテキ"], []),
        ("長男", "ちょうなん", "eldest son", ["チョウナン"], []),
        ("社会", "しゃかい", "society", ["シャカイ"], []),
        ("長女", "ちょうじょ", "eldest daughter", ["チョウジョ"], []),
    ],
    # Lesson 304[cite: 34]
    [
        ("仕上がる", "しあがる", "to be finished / completed", [], ["しあ.がる"]),
        ("重大", "じゅうだい", "serious / important / grave", ["ジュウダイ"], []),
        ("出前", "でまえ", "home delivery (food)", [], ["でまえ"]),
        ("大げさ", "おおげさ", "exaggerated / grandiose", [], ["おおげさ"]),
    ],
    # Lesson 305[cite: 34]
    [
        ("冬物", "ふゆもの", "winter clothing/goods", [], ["ふゆもの"]),
        ("見送る", "みおくる", "to see someone off", [], ["みおく.る"]),
        ("学年", "がくねん", "school year / grade", ["ガクネン"], []),
        ("三男", "さんなん", "third son", ["サンナン"], []),
    ],
    # Lesson 306[cite: 34]
    [
        ("不安", "ふあん", "anxiety / uneasiness", ["フアン"], []),
        ("なまけ者", "なまけもの", "lazy person / sloth", [], ["なまけもの"]),
        ("水着", "みずぎ", "swimsuit", [], ["みずぎ"]),
        ("長生き", "ながいき", "longevity / long life", [], ["ながいき"]),
    ],
    # Lesson 307[cite: 34]
    [
        ("地方", "ちほう", "region / district / countryside", ["チホウ"], []),
        ("早め", "はやめ", "early / ahead of time", ["ソウ"], ["はや.め"]),
        ("入門", "にゅうもん", "entering an institution / primer", ["ニュウモン"], []),
        ("正答", "せいとう", "correct answer", ["セイトウ"], []),
    ],
    # Lesson 308[cite: 34]
    [
        ("仕上げる", "しあげる", "to finish up / complete", [], ["しあ.げる"]),
        ("夜ふかし", "よふかし", "staying up late", [], ["よふかし"]),
        ("三女", "さんじょ", "third daughter", ["サンジョ"], []),
        ("見本", "みほん", "sample / model", [], ["みほん"]),
    ],
    # Lesson 309[cite: 34]
    [
        ("あて名", "あてな", "addressee's name", [], ["あてな"]),
        ("通学", "つうがく", "commuting to school", ["ツウガク"], []),
        ("出会う", "であう", "to meet by chance / encounter", [], ["であ.う"]),
        ("無意味", "むいみ", "meaningless / senseless", ["ムイミ"], []),
    ],
    # Lesson 310[cite: 34]
    [
        ("日帰り", "ひがえり", "day trip", [], ["ひがえり"]),
        ("無計画", "むけいかく", "unplanned / haphazard", ["ムケイカク"], []),
        ("気楽", "きらく", "carefree / comfortable / easy", ["キラク"], []),
        ("以後", "いご", "after this / hereafter", ["イゴ"], []),
    ],
    # Lesson 311[cite: 34]
    [
        ("真っ黒", "まっくろ", "pitch black", ["マックロ"], []),
        ("読書", "どくしょ", "reading books", ["ドクショ"], []),
        ("言語学", "げんごがく", "linguistics", ["ゲンゴガク"], []),
        ("目立つ", "めだつ", "to stand out / be conspicuous", [], ["めだ.つ"]),
    ],
    # Lesson 312[cite: 34]
    [
        ("真っ青", "まっさお", "deep blue / pale", ["マッサオ"], []),
        ("気にする", "きにする", "to mind / care about / worry", [], ["きにす.る"]),
        ("真夏日", "まなつび", "midsummer day (over 30°C)", [], ["まなつび"]),
        ("夕食", "ゆうしょく", "evening meal / dinner", ["ユウショク"], []),
    ],
    # Lesson 313[cite: 34]
    [
        ("心から", "こころから", "from the bottom of one's heart", [], ["こころから"]),
        ("行方不明", "ゆくえふめい", "missing / whereabouts unknown", ["ユクエフメイ"], []),
        ("日の出", "ひので", "sunrise", [], ["ひので"]),
        ("一気に", "いっきに", "in one breath / all at once", ["イッキ"], []),
    ],
    # Lesson 314[cite: 34]
    [
        ("元日", "がんじつ", "New Year's Day", ["ガンジツ"], []),
        ("手間", "てま", "time / labor / trouble", [], ["てま"]),
        ("気に入る", "きにいる", "to be pleased with / like", [], ["きにい.る"]),
        ("日帰り旅行", "ひがえりりょこう", "day trip", [], ["ひがえりりょこう"]),
    ],
    # Lesson 315[cite: 34]
    [
        ("一言", "ひとこと", "single word / brief remark", ["イチゲン"], ["ひとこと"]),
        ("下品", "げひん", "vulgar / coarse / indecent", ["ゲヒン"], []),
        ("発見者", "はっけんしゃ", "discoverer / finder", ["ハッケンシャ"], []),
    ],
    # Lesson 316[cite: 34]
    [
        ("自動ドア", "じどうドア", "automatic door", ["ジドウ"], []),
        ("大きめ", "おおきめ", "on the large side", ["ダイ"], ["おお.きめ"]),
        ("特売品", "とくばいひん", "bargain item / special sale item", ["トクバイヒン"], []),
        ("私立", "しりつ", "private (institution)", ["シリツ"], []),
    ],
    # Lesson 317[cite: 34]
    [
        ("知人", "ちじん", "acquaintance", ["チジン"], []),
        ("自動的", "じどうてき", "automatic", ["ジドウテキ"], []),
        ("先日", "せんじつ", "the other day / a few days ago", ["センジツ"], []),
        ("小雨", "こさめ", "light rain / drizzle", [], ["こさめ"]),
    ],
    # Lesson 318[cite: 34]
    [
        ("貸し出し", "かしだし", "lending / loaning", [], ["かしだし"]),
        ("近道", "ちかみち", "shortcut", [], ["ちかみち"]),
        ("口ぐせ", "くちぐせ", "habit of saying / catchphrase", [], ["くちぐせ"]),
        ("下る", "くだる", "to descend / go down", ["カ", "ゲ"], ["くだ.る", "さ.がる"]),
    ],
    # Lesson 319[cite: 34]
    [
        ("味方", "みかた", "friend / ally / supporter", ["ミカタ"], []),
        ("八百屋", "やおや", "greengrocer", [], ["やおや"]),
        ("電子レンジ", "でんしレンジ", "microwave oven", ["デンシ"], []),
        ("見送り", "みおくり", "seeing someone off / send-off", [], ["みおくり"]),
    ],
    # Lesson 320[cite: 34]
    [
        ("大雨", "おおあめ", "heavy rain", [], ["おおあめ"]),
        ("注目", "ちゅうもく", "notice / attention", ["チュウモク"], []),
        ("外す", "はずす", "to unfasten / remove / miss", ["ガイ"], ["はず.す"]),
        ("送別会", "そうべつかい", "farewell party", ["ソウベツカイ"], []),
    ],
    # Lesson 321[cite: 35]
    [
        ("通りかかる", "とおりかかる", "to happen to pass by", [], ["とおりかか.る"]),
        ("思い切り", "おもいきり", "with all one's might / to heart's content", [], ["おもいきり"]),
        ("日の入り", "ひのいり", "sunset", [], ["ひのいり"]),
        ("作家", "さっか", "author / writer / novelist", ["サッカ"], []),
    ],
    # Lesson 322[cite: 35]
    [
        ("休館日", "きゅうかんび", "museum/library closing day", ["キュウカンビ"], []),
        ("特長", "とくちょう", "strong point / merit", ["トクチョウ"], []),
        ("出身地", "しゅっしんち", "birthplace / hometown", ["シュッシンチ"], []),
        ("いつの間にか", "いつのまにか", "before one knows it", [], ["いつのまにか"]),
    ],
    # Lesson 323[cite: 35]
    [
        ("下書き", "したがき", "rough draft", [], ["したがき"]),
        ("送料", "そうりょう", "postage / shipping fee", ["ソウリョウ"], []),
        ("後半", "こうはん", "second half", ["コウハン"], []),
        ("計画的", "けいかくてき", "planned / systematic", ["ケイカクテキ"], []),
    ],
    # Lesson 324[cite: 35]
    [
        ("姉妹", "しまい", "sisters", ["シマイ"], []),
        ("建て前", "たてまえ", "public stance / principle", [], ["たてまえ"]),
        ("広がる", "ひろがる", "to spread out / extend", ["コウ"], ["ひろ.がる", "ひろ.げる"]),
        ("下り", "くだり", "down-train / going down", ["カ"], ["くだ.り"]),
    ],
    # Lesson 325[cite: 35]
    [
        ("工業", "こうぎょう", "manufacturing industry", ["コウギョウ"], []),
        ("小さめ", "ちいさめ", "on the small side", ["ショウ"], ["ちい.さめ"]),
        ("見物", "けんぶつ", "sightseeing", ["ケンブツ"], []),
        ("少なめ", "すくなめ", "somewhat scarce / small amount", ["ショウ"], ["すく.なめ"]),
    ],
    # Lesson 326[cite: 35]
    [
        ("画家", "がか", "painter / artist", ["ガカ"], []),
        ("終電", "しゅうでん", "last train", ["シュウデン"], []),
        ("上り", "のぼり", "up-train / ascent", ["ジョウ"], ["のぼ.り"]),
        ("国語", "こくご", "national language / Japanese", ["コクゴ"], []),
    ],
    # Lesson 327[cite: 35]
    [
        ("生意気", "なまいき", "impertinent / cheeky", ["ナマイキ"], []),
        ("水族館", "すいぞくかん", "aquarium", ["スイゾクカン"], []),
        ("中古車", "ちゅうこしゃ", "used car / secondhand car", ["チュウコシャ"], []),
        ("一人っ子", "ひとりっこ", "only child", [], ["ひとりっこ"]),
    ],
    # Lesson 328[cite: 35]
    [
        ("一方通行", "いっぽうつうこう", "one-way traffic", ["イッポウツウコウ"], []),
        ("公立", "こうりつ", "public (school/institution)", ["コウリツ"], []),
        ("一体", "いったい", "what on earth / one body", ["イッタイ"], []),
        ("以来", "いらい", "since / henceforth", ["イライ"], []),
    ],
    # Lesson 329[cite: 35]
    [
        ("発車", "はっしゃ", "departure of a vehicle", ["ハッシャ"], []),
        ("売り切れる", "うりきれる", "to be sold out", [], ["うりき.れる"]),
        ("広げる", "ひろげる", "to spread / expand / open", ["コウ"], ["ひろ.げる"]),
        ("品切れ", "しなぎれ", "out of stock", [], ["しなぎれ"]),
    ],
    # Lesson 330[cite: 35]
    [
        ("持ち物", "もちもの", "personal belongings", [], ["もちもの"]),
        ("通知", "つうち", "notice / notification", ["ツウチ"], []),
        ("見上げる", "みあげる", "to look up at", [], ["みあ.げる"]),
        ("人ごみ", "ひとごみ", "crowd of people", [], ["ひとごみ"]),
    ],
    # Lesson 331[cite: 35]
    [
        ("乗用", "じょうよう", "for riding / passenger use", ["ジョウヨウ"], []),
        ("見かける", "みかける", "to happen to see / notice", [], ["みか.ける"]),
        ("水分", "すいぶん", "moisture / water content", ["スイブン"], []),
        ("小さじ", "こさじ", "teaspoon", [], ["こさじ"]),
    ],
    # Lesson 332[cite: 35]
    [
        ("来日", "らいにち", "visit/arrival in Japan", ["ライニチ"], []),
        ("一昨日", "おととい", "day before yesterday", [], ["おととい"]),
        ("集中", "しゅうちゅう", "concentration", ["シュウチュウ"], []),
        ("社会人", "しゃかいじん", "working adult / member of society", ["シャカイジン"], []),
    ],
    # Lesson 333[cite: 35]
    [
        ("食品", "しょくひん", "foodstuff / groceries", ["ショクヒン"], []),
        ("多少", "たしょう", "more or less / somewhat", ["タショウ"], []),
        ("外食", "がいしょく", "eating out", ["ガイショク"], []),
        ("意地悪", "いじわる", "malicious / ill-tempered", ["イジワル"], []),
    ],
    # Lesson 334[cite: 35]
    [
        ("私たち", "わたしたち", "we / us", [], ["わたしたち"]),
        ("発生", "はっせい", "outbreak / occurrence", ["ハッセイ"], []),
        ("強力", "きょうりょく", "powerful / strong", ["キョウリョク"], []),
        ("語る", "かたる", "to talk / tell / narrate", ["ゴ"], ["かた.る"]),
    ],
    # Lesson 335[cite: 35]
    [
        ("運", "うん", "fortune / luck", ["ウン"], ["はこ.ぶ"]),
        ("分ける", "わける", "to divide / separate / share", ["ブン", "フン"], ["わ.ける"]),
        ("使用", "しよう", "use / application", ["シヨウ"], []),
        ("世界的", "せかいてき", "worldwide / global", ["セカイテキ"], []),
    ],
    # Lesson 336[cite: 35]
    [
        ("物理学", "ぶつりがく", "physics", ["ブツリガク"], []),
        ("親子", "おやこ", "parent and child", [], ["おやこ"]),
        ("心理学", "しんりがく", "psychology", ["シンリガク"], []),
        ("火山", "かざん", "volcano", ["カザン"], []),
    ],
    # Lesson 337[cite: 35]
    [
        ("乾杯", "かんぱい", "cheers / toast", ["カンパイ"], []),
        ("近づく", "ちかづく", "to approach / get near", ["キン"], ["ちか.づく"]),
        ("一回", "いっかい", "once / one time", ["イッカイ"], []),
        ("二回", "にかい", "twice / two times", ["ニカイ"], []),
    ],
    # Lesson 338[cite: 35]
    [
        ("三回", "さんかい", "three times", ["サンカイ"], []),
        ("四回", "よんかい", "four times", ["ヨンカイ"], []),
        ("五回", "ごかい", "five times", ["ゴカイ"], []),
        ("六回", "ろっかい", "six times", ["ロッカイ"], []),
    ],
    # Lesson 339[cite: 35]
    [
        ("七回", "ななかい", "seven times", ["ナナカイ"], []),
        ("八回", "はちかい", "eight times", ["ハチカイ"], []),
        ("九回", "きゅうかい", "nine times", ["キュウカイ"], []),
        ("十回", "じゅっかい", "ten times", ["ジュッカイ"], []),
    ],
    # Lesson 340[cite: 35]
    [
        ("一歳", "いっさい", "one year old", ["イッサイ"], []),
        ("二歳", "にさい", "two years old", ["ニサイ"], []),
        ("三歳", "さんさい", "three years old", ["サンサイ"], []),
        ("五歳", "ごさい", "five years old", ["ゴサイ"], []),
    ],
    # Lesson 341[cite: 35]
    [
        ("六歳", "ろくさい", "six years old", ["ロクサイ"], []),
        ("七歳", "ななさい", "seven years old", ["ナナサイ"], []),
        ("八歳", "はっさい", "eight years old", ["ハッサイ"], []),
        ("九歳", "きゅうさい", "nine years old", ["キュウサイ"], []),
    ],
    # Lesson 342[cite: 35]
    [
        ("十歳", "じゅっさい", "ten years old", ["ジュッサイ"], []),
        ("二十歳", "はたち", "twenty years old", [], ["はたち"]),
        ("一杯", "いっぱい", "one cup/glass / full", ["イッパイ"], []),
        ("二杯", "にはい", "two cups/glasses", ["ニハイ"], []),
    ],
    # Lesson 343[cite: 36]
    [
        ("三杯", "さんばい", "three cups/glasses", ["サンバイ"], []),
        ("四杯", "よんはい", "four cups/glasses", ["ヨンハイ"], []),
        ("五杯", "ごはい", "five cups/glasses", ["ゴハイ"], []),
    ],
    # Lesson 344[cite: 36]
    [
        ("七杯", "ななはい", "seven cups/glasses", ["ナナハイ"], []),
        ("八杯", "はっぱい", "eight cups/glasses", ["ハッパイ"], []),
        ("九杯", "きゅうはい", "nine cups/glasses", ["キュウハイ"], []),
    ],
    # Lesson 345[cite: 36]
    [
        ("十杯", "じゅっぱい", "ten cups/glasses", ["ジュッパイ"], []),
        ("何杯", "なんばい", "how many cups/glasses", ["ナンバイ"], []),
        ("売り切れ", "うりきれ", "sold out", [], ["うりきれ"]),
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
        raise FileNotFoundError(f"Run 'python generate_n3_part1.py' first to create {PART1_JSON_PATH}.")

    with open(PART1_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N3_PART2_DATA):
        lesson_num = 176 + l_idx
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

    os.makedirs(os.path.dirname(OUTPUT_TS_PATH), exist_ok=True)
    ts_content = (
        "import type { KanjiLesson } from '../types/kanji';\n\n"
        f"export const N3_LESSONS: KanjiLesson[] = {json.dumps(lessons, ensure_ascii=False, indent=2)};\n"
    )

    with open(OUTPUT_TS_PATH, "w", encoding="utf-8") as f:
        f.write(ts_content)

    # Clean up temporary part1 json
    os.remove(PART1_JSON_PATH)
    print(f"Done! Compiled all {len(lessons)} N3 lessons ({item_counter - 1} items) into {OUTPUT_TS_PATH}.")


if __name__ == "__main__":
    main()